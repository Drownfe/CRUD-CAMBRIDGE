from flask import Blueprint, request, jsonify
from models import db, Oficina, Area
from sqlalchemy.exc import IntegrityError

# Definir blueprint
oficinas_bp = Blueprint("oficinas", __name__, url_prefix="/api/oficinas")

# ==========================
# GET - Listar oficinas
# ==========================
@oficinas_bp.route("", methods=["GET"])
def get_oficinas():
    oficinas = Oficina.query.all()
    return jsonify([o.to_dict() for o in oficinas])

# ==========================
# POST - Crear oficina
# ==========================
@oficinas_bp.route("", methods=["POST"])
def add_oficina():
    data = request.json
    codigo = data.get("codigo", "").strip().title()
    id_area = data.get("idArea")

    # Validación de longitud
    if len(codigo) < 2 or len(codigo) > 100:
        return jsonify({
            "status": "error",
            "message": "⚠️ El código de la oficina debe tener entre 2 y 100 caracteres."
        }), 400

    # Validación: área debe existir
    if not Area.query.get(id_area):
        return jsonify({
            "status": "error",
            "message": "⚠️ El área seleccionada no existe."
        }), 400

    # Validación: unicidad (codigo + id_area)
    existente = Oficina.query.filter(
        Oficina.codigo.ilike(codigo),
        Oficina.id_area == id_area
    ).first()
    if existente:
        return jsonify({
            "status": "error",
            "message": "⚠️ Ya existe una oficina con ese código en el área seleccionada."
        }), 400

    nueva_oficina = Oficina(codigo=codigo, id_area=id_area)
    db.session.add(nueva_oficina)
    db.session.commit()

    return jsonify({
        "status": "ok",
        "message": "Oficina agregada con éxito ✅",
        "oficina": nueva_oficina.to_dict()
    }), 201

# ==========================
# PUT - Actualizar oficina
# ==========================
@oficinas_bp.route("/<int:id>", methods=["PUT"])
def update_oficina(id):
    oficina = Oficina.query.get_or_404(id)
    data = request.json

    codigo = data.get("codigo", "").strip().title()
    id_area = data.get("idArea")

    # Validación de longitud
    if len(codigo) < 2 or len(codigo) > 100:
        return jsonify({
            "status": "error",
            "message": "⚠️ El código de la oficina debe tener entre 2 y 100 caracteres."
        }), 400

    # Validación: área debe existir
    if id_area and not Area.query.get(id_area):
        return jsonify({
            "status": "error",
            "message": "⚠️ El área seleccionada no existe."
        }), 400

    # Validación: unicidad (codigo + id_area)
    existente = Oficina.query.filter(
        Oficina.codigo.ilike(codigo),
        Oficina.id_area == (id_area if id_area else oficina.id_area),
        Oficina.id_oficina != id
    ).first()
    if existente:
        return jsonify({
            "status": "error",
            "message": "⚠️ Ya existe otra oficina con ese código en el área seleccionada."
        }), 400

    oficina.codigo = codigo
    if id_area:
        oficina.id_area = id_area

    db.session.commit()

    return jsonify({
        "status": "ok",
        "message": "Oficina actualizada con éxito ✅",
        "oficina": oficina.to_dict()
    })

# ==========================
# DELETE - Eliminar oficina
# ==========================
@oficinas_bp.route("/<int:id>", methods=["DELETE"])
def delete_oficina(id):
    oficina = Oficina.query.get_or_404(id)
    try:
        db.session.delete(oficina)
        db.session.commit()
        return jsonify({
            "status": "ok",
            "message": "Oficina eliminada con éxito 🗑️"
        })
    except IntegrityError:
        db.session.rollback()
        return jsonify({
            "status": "error",
            "message": "⚠️ No se puede eliminar la oficina porque tiene empleados asociados."
        }), 400
