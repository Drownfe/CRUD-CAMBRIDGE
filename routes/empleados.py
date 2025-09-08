from flask import Blueprint, request, jsonify
from models import db, Empleado, Area, Oficina
from sqlalchemy.exc import IntegrityError

# Definir blueprint
empleados_bp = Blueprint("empleados", __name__, url_prefix="/api/empleados")

# ==========================
# GET - Listar empleados
# ==========================
@empleados_bp.route("", methods=["GET"])
def get_empleados():
    empleados = Empleado.query.all()
    return jsonify([e.to_dict() for e in empleados])

# ==========================
# POST - Crear empleado
# ==========================
@empleados_bp.route("", methods=["POST"])
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
        return jsonify({"status": "error", "message": "⚠️ La identificación es obligatoria."}), 400

    existente = Empleado.query.filter_by(identificacion=identificacion).first()
    if existente:
        return jsonify({"status": "error", "message": "⚠️ Ya existe un empleado con esa identificación."}), 400

    # Validación: nombre mínimo
    if len(nombre) < 3:
        return jsonify({"status": "error", "message": "⚠️ El nombre debe tener al menos 3 caracteres."}), 400

    # Validación: área y oficina existen
    if not Area.query.get(id_area):
        return jsonify({"status": "error", "message": "⚠️ El área seleccionada no existe."}), 400

    if not Oficina.query.get(id_oficina):
        return jsonify({"status": "error", "message": "⚠️ La oficina seleccionada no existe."}), 400

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

# ==========================
# PUT - Actualizar empleado
# ==========================
@empleados_bp.route("/<int:id>", methods=["PUT"])
def update_empleado(id):
    empleado = Empleado.query.get_or_404(id)
    data = request.json

    identificacion = data.get("identificacion", "").strip()
    nombre = data.get("nombre", "").strip().title()
    tipo = data.get("tipo", "").strip()
    subtipo = data.get("subtipo", "").strip()
    id_area = data.get("idArea")
    id_oficina = data.get("idOficina")

    # Validar identificación única
    if identificacion:
        existente = Empleado.query.filter(
            Empleado.identificacion == identificacion,
            Empleado.id_empleado != id
        ).first()
        if existente:
            return jsonify({"status": "error", "message": "⚠️ Otro empleado ya tiene esa identificación."}), 400
        empleado.identificacion = identificacion

    # Validar nombre
    if len(nombre) < 3:
        return jsonify({"status": "error", "message": "⚠️ El nombre debe tener al menos 3 caracteres."}), 400

    empleado.nombre = nombre
    empleado.tipo = tipo
    empleado.subtipo = subtipo

    # Validar área y oficina
    if id_area and not Area.query.get(id_area):
        return jsonify({"status": "error", "message": "⚠️ El área seleccionada no existe."}), 400
    if id_oficina and not Oficina.query.get(id_oficina):
        return jsonify({"status": "error", "message": "⚠️ La oficina seleccionada no existe."}), 400

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

# ==========================
# DELETE - Eliminar empleado
# ==========================
@empleados_bp.route("/<int:id>", methods=["DELETE"])
def delete_empleado(id):
    empleado = Empleado.query.get_or_404(id)
    try:
        db.session.delete(empleado)
        db.session.commit()
        return jsonify({"status": "ok", "message": "Empleado eliminado con éxito 🗑️"})
    except IntegrityError:
        db.session.rollback()
        return jsonify({
            "status": "error",
            "message": "⚠️ No se puede eliminar el empleado porque tiene dependencias asociadas."
        }), 400
