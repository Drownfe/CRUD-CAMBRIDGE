from flask import Blueprint, request, jsonify
from models import db, Salon, Area
from sqlalchemy.exc import IntegrityError

salones_bp = Blueprint("salones", __name__)

# Obtener todos los salones
@salones_bp.route("/api/salones", methods=["GET"])
def get_salones():
    salones = Salon.query.all()
    return jsonify([s.to_dict() for s in salones])

# Crear un salón
@salones_bp.route("/api/salones", methods=["POST"])
def add_salon():
    data = request.json
    codigo = data.get("codigo")
    id_area = data.get("idArea")

    if not codigo or not id_area:
        return jsonify({"error": "Faltan datos"}), 400

    # Validar que el área exista
    if not Area.query.get(id_area):
        return jsonify({"error": "El área no existe"}), 400

    nuevo_salon = Salon(codigo=codigo, id_area=id_area)
    db.session.add(nuevo_salon)

    try:
        db.session.commit()
        return jsonify(nuevo_salon.to_dict()), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "El código del salón ya existe"}), 400

# Actualizar salón
@salones_bp.route("/api/salones/<int:id>", methods=["PUT"])
def update_salon(id):
    salon = Salon.query.get_or_404(id)
    data = request.json
    salon.codigo = data.get("codigo", salon.codigo)
    salon.id_area = data.get("idArea", salon.id_area)

    try:
        db.session.commit()
        return jsonify(salon.to_dict())
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Error al actualizar salón"}), 400

# Eliminar salón
@salones_bp.route("/api/salones/<int:id>", methods=["DELETE"])
def delete_salon(id):
    salon = Salon.query.get_or_404(id)
    try:
        db.session.delete(salon)
        db.session.commit()
        return jsonify({"message": "Salón eliminado"}), 200
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "No se puede eliminar el salón, tiene dependencias"}), 400
