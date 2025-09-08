from flask import Blueprint, request, jsonify
from models import db, Area
from sqlalchemy.exc import IntegrityError

# Definir blueprint
areas_bp = Blueprint("areas", __name__, url_prefix="/api/areas")

# ==========================
# GET - Listar todas las áreas
# ==========================
@areas_bp.route("", methods=["GET"])
def get_areas():
    areas = Area.query.all()
    return jsonify([a.to_dict() for a in areas])

# ==========================
# POST - Crear nueva área
# ==========================
@areas_bp.route("", methods=["POST"])
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

# ==========================
# PUT - Actualizar área
# ==========================
@areas_bp.route("/<int:id>", methods=["PUT"])
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

    # Validación de unicidad (ignorando el área actual)
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

# ==========================
# DELETE - Eliminar área
# ==========================
@areas_bp.route("/<int:id>", methods=["DELETE"])
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
