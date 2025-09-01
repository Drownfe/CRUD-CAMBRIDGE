from flask import Flask, render_template, request, jsonify
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from bson import ObjectId
import os

app = Flask(__name__)

# ==============================
#   Conexión a MongoDB Atlas
# ==============================
uri = "mongodb+srv://juanhernandez82161_db_user:3113700254@colegiocambridgecluster.trcaxho.mongodb.net/?retryWrites=true&w=majority&appName=ColegioCambridgeCluster"
client = MongoClient(uri, server_api=ServerApi('1'))
db = client["CAMBRIDGE_DB"]

# Colecciones
areas_collection = db["areas"]
empleados_collection = db["empleados"]
oficinas_collection = db["oficinas"]
salones_collection = db["salones"]

# ==============================
#   Rutas de vistas (Front de Flask)
# ==============================
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/areas')
def areas_view():
    return render_template('areas.html')

@app.route('/empleados')
def empleados_view():
    return render_template('empleados.html')

@app.route('/oficinas')
def oficinas_view():
    return render_template('oficinas.html')

@app.route('/salones')
def salones_view():
    return render_template('salones.html')


# ==============================
#   API REST - ÁREAS (CRUD)
# ==============================

# READ (obtener todas las áreas)
@app.route('/api/areas', methods=['GET'])
def api_get_areas():
    areas = list(areas_collection.find({}, {"nombre": 1, "oficinas": 1}))
    for area in areas:
        area["_id"] = str(area["_id"])  # convertir ObjectId a string
    return jsonify(areas)


# CREATE (insertar nueva área)
@app.route('/api/areas', methods=['POST'])
def api_create_area():
    data = request.json
    if not data or "nombre" not in data:
        return {"message": "Datos incompletos"}, 400
    areas_collection.insert_one(data)
    return {"message": "Área creada"}, 201


# UPDATE (editar un área por ID)
@app.route('/api/areas/<string:id>', methods=['PUT'])
def api_update_area(id):
    data = request.json
    result = areas_collection.update_one(
        {"_id": ObjectId(id)},
        {"$set": data}
    )
    if result.modified_count > 0:
        return {"message": "Área actualizada"}
    return {"message": "Área no encontrada"}, 404


# DELETE (eliminar un área por ID)
@app.route('/api/areas/<string:id>', methods=['DELETE'])
def api_delete_area(id):
    result = areas_collection.delete_one({"_id": ObjectId(id)})
    if result.deleted_count > 0:
        return {"message": "Área eliminada"}
    return {"message": "Área no encontrada"}, 404


# ==============================
#   Run App
# ==============================
if __name__ == '__main__':
    app.run(debug=True)
