from flask import Blueprint, request, jsonify
from models import db, Salon, Area
from sqlalchemy.exc import IntegrityError

# Definir blueprint
salones_bp = Blueprint("salones", __name__, url_prefix="/api/salones")

# ==========================
# GET - Listar salones
# ==========================
@salones_bp.route("", methods=["GET"])
def get_salones():
    salones = Salon.query.all()
    return jsonify([s.to_dict() for s in salones])

# ==========================
# POST - Crear salón
# ==========================
@salones_bp.route("", methods=["POST"])
def add_salon():
    data = request.json
    codigo = data.get("codigo", "").strip().upper()
    id_area = data.get("idArea")

    # Validación: longitud
    if len(codigo) < 2 or len(codigo) > 50:
        return jsonify({
            "status": "error",
            "message": "⚠️ El código del salón debe tener entre 2 y 50 caracteres."
        }), 400

    # Validación: unicidad
    existente = Salon.query.filter_by(codigo=codigo).first()
    if existente:
        return jsonify({
            "status": "error",
            "message": "⚠️ Ya existe un salón con ese código."
        }), 400

    # Validación: área debe existir
    if not Area.query.get(id_area):
        return jsonify({
            "status": "error",
            "message": "⚠️ El área seleccionada no existe."
        }), 400

    nuevo_salon = Salon(codigo=codigo, id_area=id_area)
    db.session.add(nuevo_salon)
    db.session.commit()

    return jsonify({
        "status": "ok",
        "message": "Salón agregado con éxito ✅",
        "salon": nuevo_salon.to_dict()
    }), 201

# ==========================
# PUT - Actualizar salón
# ==========================
@salones_bp.route("/<int:id>", methods=["PUT"])
def update_salon(id):
    salon = Salon.query.get_or_404(id)
    data = request.json

    codigo = data.get("codigo", "").strip().upper()
    id_area = data.get("idArea")

    # Validación: longitud
    if len(codigo) < 2 or len(codigo) > 50:
        return jsonify({
            "status": "error",
            "message": "⚠️ El código del salón debe tener entre 2 y 50 caracteres."
        }), 400

    # Validación: unicidad (ignora el salón actual)
    existente = Salon.query.filter(
        Salon.codigo.ilike(codigo),
        Salon.id_salon != id
    ).first()
    if existente:
        return jsonify({
            "status": "error",
            "message": "⚠️ Ya existe otro salón con ese código."
        }), 400

    # Validación: área debe existir
    if id_area and not Area.query.get(id_area):
        return jsonify({
            "status": "error",
            "message": "⚠️ El área seleccionada no existe."
        }), 400

    salon.codigo = codigo
    if id_area:
        salon.id_area = id_area

    db.session.commit()

    return jsonify({
        "status": "ok",
        "message": "Salón actualizado con éxito ✅",
        "salon": salon.to_dict()
    })

# ==========================
# DELETE - Eliminar salón
# ==========================
@salones_bp.route("/<int:id>", methods=["DELETE"])
def delete_salon(id):
    salon = Salon.query.get_or_404(id)
    try:
        db.session.delete(salon)
        db.session.commit()
        return jsonify({
            "status": "ok",
            "message": "Salón eliminado con éxito 🗑️"
        })
    except IntegrityError:
        db.session.rollback()
        return jsonify({
            "status": "error",
            "message": "⚠️ No se puede eliminar el salón porque tiene dependencias asociadas."
        }), 400
