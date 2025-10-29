# graphql_schema.py
from ariadne import QueryType, MutationType, ObjectType, make_executable_schema, gql
from models import db, Area, Oficina, Empleado, Salon
from utils.export_excel import (
    export_areas_xlsx, export_oficinas_xlsx, export_empleados_xlsx, export_salones_xlsx
)

# --- Definición del schema (tipos, queries, mutations) ---
type_defs = gql("""
  type Area { id: ID! nombre: String! oficinas: [Oficina!]! empleados: [Empleado!]! salones: [Salon!]! }
  type Oficina { id: ID! codigo: String! idArea: Int! area: Area! }
  type Empleado { id: ID! identificacion: String! nombre: String! tipo: String subtipo: String idArea: Int idOficina: Int area: Area oficina: Oficina }
  type Salon { id: ID! codigo: String! idArea: Int! area: Area! }

  type MutationPayload {
    ok: Boolean!
    message: String
    exportUrl: String
    area: Area
    empleado: Empleado
    oficina: Oficina
    salon: Salon
  }

  type Query {
    areas: [Area!]!
    oficinas: [Oficina!]!
    empleados: [Empleado!]!
    salones: [Salon!]!
    area(id: ID!): Area
    empleado(id: ID!): Empleado
    reporteAreasEmpleados: [AreaReporte!]!
  }

  input NuevaAreaInput { nombre: String! }
  input EditarAreaInput { id: ID!, nombre: String! }
  input NuevoEmpleadoInput {
    identificacion: String!
    nombre: String!
    tipo: String
    subtipo: String
    idArea: Int!
    idOficina: Int!
  }
  input EditarEmpleadoInput {
    id: ID!
    identificacion: String
    nombre: String
    tipo: String
    subtipo: String
    idArea: Int
    idOficina: Int
  }

  type AreaReporte { id: ID! nombre: String! empleados: [Empleado!]! }

  type Mutation {
    crearArea(data: NuevaAreaInput!): MutationPayload!
    editarArea(data: EditarAreaInput!): MutationPayload!
    eliminarArea(id: ID!): MutationPayload!

    crearEmpleado(data: NuevoEmpleadoInput!): MutationPayload!
    editarEmpleado(data: EditarEmpleadoInput!): MutationPayload!
    eliminarEmpleado(id: ID!): MutationPayload!
  }
""")


# --- Query & Mutation roots ---
query = QueryType()
mutation = MutationType()

# --- Mapeadores a dict (evita depender de to_dict) ---
def area_to_dict(a: Area):
    return {"id": a.id_area, "nombre": a.nombre}

def oficina_to_dict(o: Oficina):
    return {"id": o.id_oficina, "codigo": o.codigo, "idArea": o.id_area}

def empleado_to_dict(e: Empleado):
    return {
        "id": e.id_empleado,
        "identificacion": e.identificacion,
        "nombre": e.nombre,
        "tipo": e.tipo,
        "subtipo": e.subtipo,
        "idArea": e.id_area,
        "idOficina": e.id_oficina,
    }

def salon_to_dict(s: Salon):
    return {"id": s.id_salon, "codigo": s.codigo, "idArea": s.id_area}

# --- Resolvers de Query ---
@query.field("areas")
def resolve_areas(*_):
    return [area_to_dict(a) for a in Area.query.all()]

@query.field("oficinas")
def resolve_oficinas(*_):
    return [oficina_to_dict(o) for o in Oficina.query.all()]

@query.field("empleados")
def resolve_empleados(*_):
    return [empleado_to_dict(e) for e in Empleado.query.all()]

@query.field("salones")
def resolve_salones(*_):
    return [salon_to_dict(s) for s in Salon.query.all()]

@query.field("area")
def resolve_area(*_, id):
    a = Area.query.get(int(id))
    return area_to_dict(a) if a else None

@query.field("empleado")
def resolve_empleado(*_, id):
    e = Empleado.query.get(int(id))
    return empleado_to_dict(e) if e else None

@query.field("reporteAreasEmpleados")
def resolve_reporte(*_):
    salida = []
    for a in Area.query.all():
        emps = Empleado.query.filter_by(id_area=a.id_area).all()
        salida.append({
            "id": a.id_area,
            "nombre": a.nombre,
            "empleados": [empleado_to_dict(e) for e in emps]
        })
    return salida

# --- Resolvers de campos (relaciones) ---
def resolve_area_oficinas(area_obj, *_):
    return [oficina_to_dict(o) for o in Oficina.query.filter_by(id_area=area_obj["id"]).all()]

def resolve_area_empleados(area_obj, *_):
    return [empleado_to_dict(e) for e in Empleado.query.filter_by(id_area=area_obj["id"]).all()]

def resolve_area_salones(area_obj, *_):
    return [salon_to_dict(s) for s in Salon.query.filter_by(id_area=area_obj["id"]).all()]

def resolve_oficina_area(oficina_obj, *_):
    a = Area.query.get(oficina_obj["idArea"])
    return area_to_dict(a) if a else None

def resolve_empleado_area(empleado_obj, *_):
    a = Area.query.get(empleado_obj["idArea"])
    return area_to_dict(a) if a else None

def resolve_empleado_oficina(empleado_obj, *_):
    o = Oficina.query.get(empleado_obj["idOficina"])
    return oficina_to_dict(o) if o else None

def resolve_salon_area(salon_obj, *_):
    a = Area.query.get(salon_obj["idArea"])
    return area_to_dict(a) if a else None

# --- Mutations ---
from sqlalchemy.exc import IntegrityError

@mutation.field("crearArea")
def resolve_crear_area(*_, data):
    nombre = data["nombre"].strip().title()
    if Area.query.filter(Area.nombre.ilike(nombre)).first():
        raise Exception("El área ya existe.")
    a = Area(nombre=nombre)
    db.session.add(a); db.session.commit()
    url = export_areas_xlsx()
    return {"ok": True, "area": area_to_dict(a), "exportUrl": url, "message": "Área creada y Excel generado."}

@mutation.field("editarArea")
def resolve_editar_area(*_, data):
    a = Area.query.get(int(data["id"]))
    if not a:
        raise Exception("Área no encontrada.")
    nuevo = data["nombre"].strip().title()
    if Area.query.filter(Area.nombre.ilike(nuevo), Area.id_area != a.id_area).first():
        raise Exception("Ya existe otra área con ese nombre.")
    a.nombre = nuevo
    db.session.commit()
    url = export_areas_xlsx()
    return {"ok": True, "area": area_to_dict(a), "exportUrl": url, "message": "Área actualizada y Excel generado."}

@mutation.field("eliminarArea")
def resolve_eliminar_area(*_, id):
    a = Area.query.get(int(id))
    if not a:
        return {"ok": False, "message": "Área no encontrada."}
    if Oficina.query.filter_by(id_area=a.id_area).first() \
       or Empleado.query.filter_by(id_area=a.id_area).first() \
       or Salon.query.filter_by(id_area=a.id_area).first():
        raise Exception("No se puede eliminar: tiene dependencias.")
    db.session.delete(a); db.session.commit()
    url = export_areas_xlsx()
    return {"ok": True, "exportUrl": url, "message": "Área eliminada y Excel generado."}

@mutation.field("crearEmpleado")
def resolve_crear_empleado(*_, data):
    ident = data["identificacion"].strip()
    if Empleado.query.filter_by(identificacion=ident).first():
        raise Exception("Identificación ya existe.")
    e = Empleado(
        identificacion=ident,
        nombre=data["nombre"].strip().title(),
        tipo=(data.get("tipo") or "").strip(),
        subtipo=(data.get("subtipo") or "").strip(),
        id_area=int(data["idArea"]),
        id_oficina=int(data["idOficina"])
    )
    db.session.add(e); db.session.commit()
    url = export_empleados_xlsx()
    return {"ok": True, "empleado": empleado_to_dict(e), "exportUrl": url, "message": "Empleado creado y Excel generado."}

@mutation.field("editarEmpleado")
def resolve_editar_empleado(*_, data):
    e = Empleado.query.get(int(data["id"]))
    if not e:
        return {"ok": False, "message": "Empleado no encontrado."}
    if data.get("identificacion"):
        ident = data["identificacion"].strip()
        existe = Empleado.query.filter(Empleado.identificacion == ident,
                                       Empleado.id_empleado != e.id_empleado).first()
        if existe:
            raise Exception("Otra persona ya tiene esa identificación.")
        e.identificacion = ident
    if data.get("nombre"): e.nombre = data["nombre"].strip().title()
    if "tipo" in data: e.tipo = (data.get("tipo") or "").strip()
    if "subtipo" in data: e.subtipo = (data.get("subtipo") or "").strip()
    if data.get("idArea") is not None: e.id_area = int(data["idArea"])
    if data.get("idOficina") is not None: e.id_oficina = int(data["idOficina"])
    db.session.commit()
    url = export_empleados_xlsx()
    return {"ok": True, "empleado": empleado_to_dict(e), "exportUrl": url, "message": "Empleado actualizado y Excel generado."}

@mutation.field("eliminarEmpleado")
def resolve_eliminar_empleado(*_, id):
    e = Empleado.query.get(int(id))
    if not e:
        return {"ok": False, "message": "Empleado no encontrado."}
    db.session.delete(e); db.session.commit()
    url = export_empleados_xlsx()
    return {"ok": True, "exportUrl": url, "message": "Empleado eliminado y Excel generado."}

# --- Construcción del schema ejecutable ---
# ---- ObjectType para resolvers de campos (relaciones) ----
AreaOT = ObjectType("Area")
AreaOT.set_field("oficinas", resolve_area_oficinas)
AreaOT.set_field("empleados", resolve_area_empleados)
AreaOT.set_field("salones", resolve_area_salones)

OficinaOT = ObjectType("Oficina")
OficinaOT.set_field("area", resolve_oficina_area)

EmpleadoOT = ObjectType("Empleado")
EmpleadoOT.set_field("area", resolve_empleado_area)
EmpleadoOT.set_field("oficina", resolve_empleado_oficina)

SalonOT = ObjectType("Salon")
SalonOT.set_field("area", resolve_salon_area)

# ---- Schema ejecutable correcto ----
schema = make_executable_schema(
    type_defs,
    query,
    mutation,
    AreaOT,
    OficinaOT,
    EmpleadoOT,
    SalonOT,
)
