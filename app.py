import os
from flask import Flask, jsonify, request
from flask_cors import CORS

# --- Base de datos / modelos ---
from models import db  # y tus modelos definidos en models.py (Area, Oficina, Empleado, Salon)

# --- Blueprints REST/HTML ---
from routes.areas import areas_bp
from routes.oficinas import oficinas_bp
from routes.empleados import empleados_bp
from routes.salones import salones_bp
from routes.views import views_bp  # rutas que renderizan templates

# --- GraphQL (Ariadne) ---
from ariadne import graphql_sync
# UI para navegador (según versión de Ariadne disponible)
try:
    from ariadne.explorer import ExplorerGraphiQL as ExplorerUI
except Exception:
    try:
        from ariadne.explorer import ExplorerPlayground as ExplorerUI
    except Exception:
        ExplorerUI = None

from graphql_schema import schema  # <- tu schema/resolvers de GraphQL


def create_app() -> Flask:
    app = Flask(
        __name__,
        static_folder="static",
        template_folder="templates",
    )

    # ---------------------------
    # Configuración
    # ---------------------------
    # Intenta usar tu config.py (clase Config). Si falla, usa variables de entorno.
    try:
        from config import Config  # debe existir en tu proyecto
        app.config.from_object(Config)
    except Exception:
        app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
            "SQLALCHEMY_DATABASE_URI",
            "mysql+pymysql://usuario:password@localhost/cambridge_db",
        )
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "supersecreto")

    # ---------------------------
    # Extensiones
    # ---------------------------
    CORS(app)
    db.init_app(app)

    # ---------------------------
    # Blueprints
    # ---------------------------
    app.register_blueprint(views_bp)      # rutas HTML (/  /areas  /empleados  /oficinas  /salones)
    app.register_blueprint(areas_bp)      # /api/areas
    app.register_blueprint(oficinas_bp)   # /api/oficinas
    app.register_blueprint(empleados_bp)  # /api/empleados
    app.register_blueprint(salones_bp)    # /api/salones

    # ---------------------------
    # Healthcheck sencillo
    # ---------------------------
    @app.get("/health")
    def health():
        return {"status": "ok"}

    # ---------------------------
    # Endpoint GraphQL (GET+POST)
    # ---------------------------
    @app.route("/graphql", methods=["GET", "POST"])
    def graphql_endpoint():
        # UI en navegador (GET)
        if request.method == "GET":
            if ExplorerUI:
                return ExplorerUI().html(None), 200
            return (
                "<h3>GraphQL listo</h3>"
                "<p>Envia POST con JSON: {\"query\": \"...\", \"variables\": {...}}</p>",
                200,
            )

        # Ejecución de queries/mutations (POST)
        data = request.get_json(silent=True) or {}
        success, result = graphql_sync(schema, data, context_value={"request": request})
        status = 200 if "errors" not in result else 400
        return jsonify(result), status

    return app


# ------------- Entry point -------------
app = create_app()

if __name__ == "__main__":
    # Para ejecutar con: python app.py
    app.run(host="127.0.0.1", port=5000)
