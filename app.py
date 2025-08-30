from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient

app = Flask(__name__)

# String de conexión MongoDB Atlas
uri = "mongodb+srv://juanhernandez82161_db_user:3113700254@colegiocambridgecluster.trcaxho.mongodb.net/?retryWrites=true&w=majority&appName=ColegioCambridgeCluster"
client = MongoClient(uri)
db = client['CAMBRIDGE_DB']

# Colecciones
areas_collection = db['areas']
empleados_collection = db['empleados']
oficinas_collection = db['oficinas']
salones_collection = db['salones']

# Rutas con renderización HTML

@app.route('/areas', methods=['GET'])
def get_areas():
    areas = list(areas_collection.find({}, {'_id': 0}))
    return render_template('areas.html', areas=areas)

@app.route('/empleados', methods=['GET'])
def get_empleados():
    empleados = list(empleados_collection.find({}, {'_id': 0}))
    return render_template('empleados.html', empleados=empleados)

@app.route('/oficinas', methods=['GET'])
def get_oficinas():
    oficinas = list(oficinas_collection.find({}, {'_id': 0}))
    return render_template('oficinas.html', oficinas=oficinas)

@app.route('/salones', methods=['GET'])
def get_salones():
    salones = list(salones_collection.find({}, {'_id': 0}))
    return render_template('salones.html', salones=salones)


# API REST (JSON) - CRUD básicos solo Create y Read para ejemplo

@app.route('/api/empleados', methods=['GET'])
def api_get_empleados():
    empleados = list(empleados_collection.find({}, {'_id': 0}))
    return jsonify(empleados)

@app.route('/api/empleados', methods=['POST'])
def api_create_empleado():
    data = request.json
    empleados_collection.insert_one(data)
    return {"message": "Empleado creado"}, 201

@app.route('/api/oficinas', methods=['GET'])
def api_get_oficinas():
    oficinas = list(oficinas_collection.find({}, {'_id': 0}))
    return jsonify(oficinas)

@app.route('/api/oficinas', methods=['POST'])
def api_create_oficina():
    data = request.json
    oficinas_collection.insert_one(data)
    return {"message": "Oficina creada"}, 201

@app.route('/api/salones', methods=['GET'])
def api_get_salones():
    salones = list(salones_collection.find({}, {'_id': 0}))
    return jsonify(salones)

@app.route('/api/salones', methods=['POST'])
def api_create_salon():
    data = request.json
    salones_collection.insert_one(data)
    return {"message": "Salon creado"}, 201


if __name__ == '__main__':
    app.run(debug=True)
