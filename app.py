from flask import Flask
from flask_cors import CORS
from models import db
from config import DB_URI

# Importar Blueprints de rutas
from routes.areas import areas_bp
from routes.empleados import empleados_bp
from routes.oficinas import oficinas_bp
from routes.salones import salones_bp
from routes.views import views_bp

# ==============================================
# CONFIGURACIÓN DE FLASK
# ==============================================
app = Flask(__name__, template_folder="templates", static_folder="static")

app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

CORS(app)
db.init_app(app)

# ==============================================
# REGISTRO DE RUTAS (Blueprints)
# ==============================================
app.register_blueprint(areas_bp)
app.register_blueprint(empleados_bp)
app.register_blueprint(oficinas_bp)
app.register_blueprint(salones_bp)
app.register_blueprint(views_bp)

# ==============================================
# MAIN
# ==============================================
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
