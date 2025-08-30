from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# String de conexión con el usuario y contraseña correctos
uri = "mongodb+srv://juanhernandez82161_db_user:3113700254@colegiocambridgecluster.trcaxho.mongodb.net/?retryWrites=true&w=majority&appName=ColegioCambridgeCluster"
client = MongoClient(uri, server_api=ServerApi('1'))

try:
    client.admin.command('ping')
    print("¡Conexión exitosa a MongoDB Atlas!")
except Exception as e:
    print(e)
