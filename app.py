from flask import Flask, render_template, request, jsonify
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from bson import ObjectId

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
#   Rutas de vistas
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
@app.route('/api/areas', methods=['GET'])
def api_get_areas():
    areas = list(areas_collection.find({}, {"nombre": 1, "oficinas": 1}))
    for a in areas:
        a["_id"] = str(a["_id"])
    return jsonify(areas)

@app.route('/api/areas', methods=['POST'])
def api_create_area():
    data = request.json
    if not data or "nombre" not in data:
        return {"message": "Datos incompletos"}, 400
    areas_collection.insert_one(data)
    return {"message": "Área creada"}, 201

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

@app.route('/api/areas/<string:id>', methods=['DELETE'])
def api_delete_area(id):
    result = areas_collection.delete_one({"_id": ObjectId(id)})
    if result.deleted_count > 0:
        return {"message": "Área eliminada"}
    return {"message": "Área no encontrada"}, 404

# ==============================
#   API REST - EMPLEADOS (CRUD)
# ==============================
@app.route('/api/empleados', methods=['GET'])
def api_get_empleados():
    empleados = list(empleados_collection.find({}, {
        "identificacion": 1, "nombre": 1, "tipo": 1,
        "subtipo": 1, "idArea": 1, "idOficina": 1
    }))
    for e in empleados:
        e["_id"] = str(e["_id"])
    return jsonify(empleados)

@app.route('/api/empleados', methods=['POST'])
def api_create_empleado():
    data = request.json
    if not data or "identificacion" not in data or "nombre" not in data:
        return {"message": "Datos incompletos"}, 400
    empleados_collection.insert_one(data)
    return {"message": "Empleado creado"}, 201

@app.route('/api/empleados/<string:id>', methods=['PUT'])
def api_update_empleado(id):
    data = request.json
    result = empleados_collection.update_one(
        {"_id": ObjectId(id)},
        {"$set": data}
    )
    if result.modified_count > 0:
        return {"message": "Empleado actualizado"}
    return {"message": "Empleado no encontrado"}, 404

@app.route('/api/empleados/<string:id>', methods=['DELETE'])
def api_delete_empleado(id):
    result = empleados_collection.delete_one({"_id": ObjectId(id)})
    if result.deleted_count > 0:
        return {"message": "Empleado eliminado"}
    return {"message": "Empleado no encontrado"}, 404

# ==============================
#   API REST - OFICINAS (CRUD)
# ==============================
@app.route('/api/oficinas', methods=['GET'])
def api_get_oficinas():
    oficinas = list(oficinas_collection.find({}, {"codigo": 1, "idArea": 1, "empleados": 1}))
    for o in oficinas:
        o["_id"] = str(o["_id"])
    return jsonify(oficinas)

@app.route('/api/oficinas', methods=['POST'])
def api_create_oficina():
    data = request.json
    if not data or "codigo" not in data:
        return {"message": "Datos incompletos"}, 400
    oficinas_collection.insert_one(data)
    return {"message": "Oficina creada"}, 201

@app.route('/api/oficinas/<string:id>', methods=['PUT'])
def api_update_oficina(id):
    data = request.json
    result = oficinas_collection.update_one(
        {"_id": ObjectId(id)},
        {"$set": data}
    )
    if result.modified_count > 0:
        return {"message": "Oficina actualizada"}
    return {"message": "Oficina no encontrada"}, 404

@app.route('/api/oficinas/<string:id>', methods=['DELETE'])
def api_delete_oficina(id):
    result = oficinas_collection.delete_one({"_id": ObjectId(id)})
    if result.deleted_count > 0:
        return {"message": "Oficina eliminada"}
    return {"message": "Oficina no encontrada"}, 404

# ==============================
#   API REST - SALONES (CRUD)
# ==============================
@app.route('/api/salones', methods=['GET'])
def api_get_salones():
    salones = list(salones_collection.find({}, {"codigo": 1, "idArea": 1}))
    for s in salones:
        s["_id"] = str(s["_id"])
    return jsonify(salones)

@app.route('/api/salones', methods=['POST'])
def api_create_salon():
    data = request.json
    if not data or "codigo" not in data:
        return {"message": "Datos incompletos"}, 400
    salones_collection.insert_one(data)
    return {"message": "Salón creado"}, 201

@app.route('/api/salones/<string:id>', methods=['PUT'])
def api_update_salon(id):
    data = request.json
    result = salones_collection.update_one(
        {"_id": ObjectId(id)},
        {"$set": data}
    )
    if result.modified_count > 0:
        return {"message": "Salón actualizado"}
    return {"message": "Salón no encontrado"}, 404

@app.route('/api/salones/<string:id>', methods=['DELETE'])
def api_delete_salon(id):
    result = salones_collection.delete_one({"_id": ObjectId(id)})
    if result.deleted_count > 0:
        return {"message": "Salón eliminado"}
    return {"message": "Salón no encontrado"}, 404

# ==============================
#   Run App
# ==============================
if __name__ == '__main__':
    app.run(debug=True)
