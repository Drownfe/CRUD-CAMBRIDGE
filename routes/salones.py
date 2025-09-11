from flask import Blueprint, request, jsonify
from models import db, Salon, Area
from sqlalchemy.exc import IntegrityError

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
    codigo = data.get("codigo", "").strip()
    id_area = data.get("idArea")

    if not codigo or not id_area:
        return jsonify({"status": "error", "message": "⚠️ Faltan datos"}), 400

    # Validar que el área exista
    if not Area.query.get(id_area):
        return jsonify({"status": "error", "message": "⚠️ El área no existe"}), 400

    # Validación: unicidad (codigo + id_area)
    existente = Salon.query.filter(
        Salon.codigo.ilike(codigo),
        Salon.id_area == id_area
    ).first()
    if existente:
        return jsonify({
            "status": "error",
            "message": "⚠️ Ya existe un salón con ese código en el área seleccionada."
        }), 400

    nuevo_salon = Salon(codigo=codigo, id_area=id_area)
    db.session.add(nuevo_salon)

    try:
        db.session.commit()
        return jsonify({"status": "ok", "message": "Salón agregado ✅", "salon": nuevo_salon.to_dict()}), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({"status": "error", "message": "⚠️ El código del salón ya existe"}), 400

# ==========================
# PUT - Actualizar salón
# ==========================
@salones_bp.route("/<int:id>", methods=["PUT"])
def update_salon(id):
    salon = Salon.query.get_or_404(id)
    data = request.json
    codigo = data.get("codigo", salon.codigo).strip()
    id_area = data.get("idArea", salon.id_area)

    # Validar que el área exista
    if not Area.query.get(id_area):
        return jsonify({"status": "error", "message": "⚠️ El área no existe"}), 400

    # Validación: unicidad (codigo + id_area)
    existente = Salon.query.filter(
        Salon.codigo.ilike(codigo),
        Salon.id_area == id_area,
        Salon.id_salon != id
    ).first()
    if existente:
        return jsonify({
            "status": "error",
            "message": "⚠️ Ya existe otro salón con ese código en el área seleccionada."
        }), 400

    salon.codigo = codigo
    salon.id_area = id_area

    try:
        db.session.commit()
        return jsonify({"status": "ok", "message": "Salón actualizado ✅", "salon": salon.to_dict()})
    except IntegrityError:
        db.session.rollback()
        return jsonify({"status": "error", "message": "⚠️ Error al actualizar salón"}),
