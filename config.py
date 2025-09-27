# config.py
import os
from dotenv import load_dotenv

# Carga variables desde .env (si existe)
load_dotenv()

class Config:
    # ----------------------------
    # Flask
    # ----------------------------
    SECRET_KEY = os.getenv("SECRET_KEY", "supersecreto")
    DEBUG = os.getenv("FLASK_DEBUG", "0") in ("1", "true", "True")

    # ----------------------------
    # SQLAlchemy / Base de datos
    # ----------------------------
    # Prioriza DB_URI del .env; si no existe, usa el fallback de MySQL local
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DB_URI",
        "mysql+pymysql://root:root1234@localhost/colegio_cambridge",
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        # Evita conexiones colgadas en desarrollo
        "pool_pre_ping": True,
        # Tamaños de pool razonables para dev
        "pool_recycle": 1800,
    }

    # ----------------------------
    # CORS (si usas fetch desde el front)
    # ----------------------------
    CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*")  # e.g. "http://localhost:3000"
    CORS_SUPPORTS_CREDENTIALS = os.getenv("CORS_SUPPORTS_CREDENTIALS", "0") in ("1", "true", "True")
