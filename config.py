import os
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

# ==============================================
# CONFIGURACIÓN DE BASE DE DATOS
# ==============================================
DB_URI = os.getenv(
    "DB_URI",
    "mysql+pymysql://root:root1234@localhost/colegio_cambridge"
)
