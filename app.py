from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os
from flask import Flask, render_template, request, jsonify, redirect
from sqlalchemy.exc import IntegrityError

# ==============================================
# CONFIGURACIÓN DE FLASK
# ==============================================
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, "templates"),
    static_folder=os.path.join(BASE_DIR, "static")
)

CORS(app)

# ==============================================
# CONFIGURACIÓN DE MYSQL
# ==============================================

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root1234@localhost/colegio_cambridge'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ==============================================
# MODELOS (Tablas)
# ==============================================

class Area(db.Model):
    __tablename__ = "areas"
    id_area = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100), unique=True, nullable=False)

    oficinas = db.relationship("Oficina", backref="area", cascade="all, delete", passive_deletes=True)
    empleados = db.relationship("Empleado", backref="area", cascade="all, delete", passive_deletes=True)
    salones = db.relationship("Salon", backref="area", cascade="all, delete", passive_deletes=True)

    def to_dict(self):
        return {"id": self.id_area, "nombre": self.nombre}
class Oficina(db.Model):
    __tablename__ = "oficinas"
    id_oficina = db.Column(db.Integer, primary_key=True, autoincrement=True)
    codigo = db.Column(db.String(100), unique=True, nullable=False)
    id_area = db.Column(db.Integer, db.ForeignKey("areas.id_area", ondelete="RESTRICT"), nullable=False)

    empleados = db.relationship("Empleado", backref="oficina", cascade="all, delete", passive_deletes=True)

    def to_dict(self):
        return {"id": self.id_oficina, "codigo": self.codigo, "idArea": self.id_area}
class Empleado(db.Model):
    __tablename__ = "empleados"
    id_empleado = db.Column(db.Integer, primary_key=True, autoincrement=True)
    identificacion = db.Column(db.String(50), nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    tipo = db.Column(db.String(50))
    subtipo = db.Column(db.String(50))
    id_area = db.Column(db.Integer, db.ForeignKey("areas.id_area", ondelete="RESTRICT"), nullable=False)
    id_oficina = db.Column(db.Integer, db.ForeignKey("oficinas.id_oficina", ondelete="RESTRICT"), nullable=False)

    def to_dict(self):
        return {
            "id": self.id_empleado,
            "identificacion": self.identificacion,
            "nombre": self.nombre,
            "tipo": self.tipo,
            "subtipo": self.subtipo,
            "idArea": self.id_area,
            "idOficina": self.id_oficina
        }
class Salon(db.Model):
    __tablename__ = "salones"
    id_salon = db.Column(db.Integer, primary_key=True, autoincrement=True)
    codigo = db.Column(db.String(100), unique=True, nullable=False)
    id_area = db.Column(db.Integer, db.ForeignKey("areas.id_area", ondelete="RESTRICT"), nullable=False)

    def to_dict(self):
        return {"id": self.id_salon, "codigo": self.codigo, "idArea": self.id_area}

# ==============================================
# RUTAS HTML
# ==============================================

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/areas")
def areas():
    all_areas = Area.query.order_by(Area.id_area.asc()).all()
    return render_template("Areas/areas.html", areas=all_areas)

@app.route("/empleados")
def empleados_page():
    return render_template("Empleados/empleados.html")

@app.route("/oficinas")
def oficinas_page():
    return render_template("Oficinas/oficinas.html")

@app.route("/salones")
def salones_page():
    return render_template("Salones/salones.html")

# ==============================================
# API AREAS
# ==============================================

@app.route("/api/areas", methods=["GET"])
def get_areas():
    areas = Area.query.all()
    return jsonify([a.to_dict() for a in areas])

# Crear Área
@app.route("/api/areas", methods=["POST"])
def add_area():
    data = request.json
    nombre = data.get("nombre", "").strip().title()

    # Validación de longitud
    if len(nombre) < 3 or len(nombre) > 100:
        return jsonify({
            "status": "error",
            "message": "⚠️ El nombre del área debe tener entre 3 y 100 caracteres."
        }), 400

    # Validación de unicidad
    existente = Area.query.filter(Area.nombre.ilike(nombre)).first()
    if existente:
        return jsonify({
            "status": "error",
            "message": "⚠️ El área ya existe, ingresa un nombre diferente."
        }), 400

    nueva_area = Area(nombre=nombre)
    db.session.add(nueva_area)
    db.session.commit()

    return jsonify({
        "status": "ok",
        "message": "Área agregada con éxito ✅",
        "area": nueva_area.to_dict()
    }), 201


# Actualizar Área
@app.route("/api/areas/<int:id>", methods=["PUT"])
def update_area(id):
    area = Area.query.get_or_404(id)
    data = request.json
    nuevo_nombre = data.get("nombre", "").strip().title()

    # Validación de longitud
    if len(nuevo_nombre) < 3 or len(nuevo_nombre) > 100:
        return jsonify({
            "status": "error",
            "message": "⚠️ El nombre del área debe tener entre 3 y 100 caracteres."
        }), 400

    # Validación de unicidad (ignorando el mismo área)
    existente = Area.query.filter(
        Area.nombre.ilike(nuevo_nombre),
        Area.id_area != id
    ).first()
    if existente:
        return jsonify({
            "status": "error",
            "message": "⚠️ Ya existe otra área con ese nombre."
        }), 400

    area.nombre = nuevo_nombre
    db.session.commit()

    return jsonify({
        "status": "ok",
        "message": "Área actualizada con éxito ✅",
        "area": area.to_dict()
    })


# Eliminar Área
@app.route("/api/areas/<int:id>", methods=["DELETE"])
def delete_area(id):
    area = Area.query.get_or_404(id)
    try:
        db.session.delete(area)
        db.session.commit()
        return jsonify({
            "status": "ok",
            "message": "Área eliminada con éxito 🗑️"
        })
    except IntegrityError:
        db.session.rollback()
        return jsonify({
            "status": "error",
            "message": "⚠️ No se puede eliminar el área porque tiene oficinas, empleados o salones asociados."
        }), 400

# ==========================
# API EMPLEADOS
# ==========================

@app.route("/api/empleados", methods=["GET"])
def get_empleados():
    empleados = Empleado.query.all()
    return jsonify([e.to_dict() for e in empleados])


@app.route("/api/empleados", methods=["POST"])
def add_empleado():
    data = request.json

    identificacion = data.get("identificacion", "").strip()
    nombre = data.get("nombre", "").strip().title()
    tipo = data.get("tipo", "").strip()
    subtipo = data.get("subtipo", "").strip()
    id_area = data.get("idArea")
    id_oficina = data.get("idOficina")

    # Validación: identificación obligatoria y única
    if not identificacion:
        return jsonify({
            "status": "error",
            "message": "⚠️ La identificación es obligatoria."
        }), 400

    existente = Empleado.query.filter_by(identificacion=identificacion).first()
    if existente:
        return jsonify({
            "status": "error",
            "message": "⚠️ Ya existe un empleado con esa identificación."
        }), 400

    # Validación: nombre con longitud mínima
    if len(nombre) < 3:
        return jsonify({
            "status": "error",
            "message": "⚠️ El nombre del empleado debe tener al menos 3 caracteres."
        }), 400

    # Validación: área y oficina deben existir
    if not Area.query.get(id_area):
        return jsonify({
            "status": "error",
            "message": "⚠️ El área seleccionada no existe."
        }), 400

    if not Oficina.query.get(id_oficina):
        return jsonify({
            "status": "error",
            "message": "⚠️ La oficina seleccionada no existe."
        }), 400

    nuevo_empleado = Empleado(
        identificacion=identificacion,
        nombre=nombre,
        tipo=tipo,
        subtipo=subtipo,
        id_area=id_area,
        id_oficina=id_oficina
    )

    db.session.add(nuevo_empleado)
    db.session.commit()

    return jsonify({
        "status": "ok",
        "message": "Empleado agregado con éxito ✅",
        "empleado": nuevo_empleado.to_dict()
    }), 201


@app.route("/api/empleados/<int:id>", methods=["PUT"])
def update_empleado(id):
    empleado = Empleado.query.get_or_404(id)
    data = request.json

    identificacion = data.get("identificacion", "").strip()
    nombre = data.get("nombre", "").strip().title()
    tipo = data.get("tipo", "").strip()
    subtipo = data.get("subtipo", "").strip()
    id_area = data.get("idArea")
    id_oficina = data.get("idOficina")

    # Validar identificación única (ignorando el propio empleado)
    if identificacion:
        existente = Empleado.query.filter(
            Empleado.identificacion == identificacion,
            Empleado.id_empleado != id
        ).first()
        if existente:
            return jsonify({
                "status": "error",
                "message": "⚠️ Otro empleado ya tiene esa identificación."
            }), 400
        empleado.identificacion = identificacion

    # Validar nombre
    if len(nombre) < 3:
        return jsonify({
            "status": "error",
            "message": "⚠️ El nombre debe tener al menos 3 caracteres."
        }), 400

    empleado.nombre = nombre
    empleado.tipo = tipo
    empleado.subtipo = subtipo

    # Validar área y oficina si cambiaron
    if id_area and not Area.query.get(id_area):
        return jsonify({
            "status": "error",
            "message": "⚠️ El área seleccionada no existe."
        }), 400
    if id_oficina and not Oficina.query.get(id_oficina):
        return jsonify({
            "status": "error",
            "message": "⚠️ La oficina seleccionada no existe."
        }), 400

    if id_area:
        empleado.id_area = id_area
    if id_oficina:
        empleado.id_oficina = id_oficina

    db.session.commit()

    return jsonify({
        "status": "ok",
        "message": "Empleado actualizado con éxito ✅",
        "empleado": empleado.to_dict()
    })


@app.route("/api/empleados/<int:id>", methods=["DELETE"])
def delete_empleado(id):
    empleado = Empleado.query.get_or_404(id)
    try:
        db.session.delete(empleado)
        db.session.commit()
        return jsonify({
            "status": "ok",
            "message": "Empleado eliminado con éxito 🗑️"
        })
    except IntegrityError:
        db.session.rollback()
        return jsonify({
            "status": "error",
            "message": "⚠️ No se puede eliminar el empleado porque tiene datos asociados."
        }), 400


# ==============================================
# API OFICINAS
# ==============================================

@app.route("/api/oficinas", methods=["GET"])
def get_oficinas():
    oficinas = Oficina.query.all()
    return jsonify([o.to_dict() for o in oficinas])

@app.route("/api/oficinas", methods=["POST"])
def add_oficina():
    data = request.json
    nueva_oficina = Oficina(codigo=data["codigo"], id_area=data["idArea"])
    db.session.add(nueva_oficina)
    db.session.commit()
    return jsonify(nueva_oficina.to_dict()), 201

@app.route("/api/oficinas/<int:id>", methods=["PUT"])
def update_oficina(id):
    oficina = Oficina.query.get_or_404(id)
    data = request.json
    oficina.codigo = data.get("codigo", oficina.codigo)
    oficina.id_area = data.get("idArea", oficina.id_area)
    db.session.commit()
    return jsonify(oficina.to_dict())

@app.route("/api/oficinas/<int:id>", methods=["DELETE"])
def delete_oficina(id):
    oficina = Oficina.query.get_or_404(id)
    db.session.delete(oficina)
    db.session.commit()
    return jsonify({"message": "Oficina eliminada"})

# ==============================================
# API SALONES
# ==============================================
@app.route("/api/salones", methods=["GET"])
def get_salones():
    salones = Salon.query.all()
    return jsonify([s.to_dict() for s in salones])

@app.route("/api/salones", methods=["POST"])
def add_salon():
    data = request.json
    nuevo_salon = Salon(codigo=data["codigo"], id_area=data["idArea"])
    db.session.add(nuevo_salon)
    db.session.commit()
    return jsonify(nuevo_salon.to_dict()), 201

@app.route("/api/salones/<int:id>", methods=["PUT"])
def update_salon(id):
    salon = Salon.query.get_or_404(id)
    data = request.json
    salon.codigo = data.get("codigo", salon.codigo)
    salon.id_area = data.get("idArea", salon.id_area)
    db.session.commit()
    return jsonify(salon.to_dict())

@app.route("/api/salones/<int:id>", methods=["DELETE"])
def delete_salon(id):
    salon = Salon.query.get_or_404(id)
    db.session.delete(salon)
    db.session.commit()
    return jsonify({"message": "Salón eliminado"})


# ==============================================
# MAIN
# ==============================================
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)