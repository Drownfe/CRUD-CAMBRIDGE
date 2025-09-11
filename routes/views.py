from flask import Blueprint, render_template

# Definir blueprint
views_bp = Blueprint("views", __name__)

# ==========================
# Rutas HTML principales
# ==========================

@views_bp.route("/")
def index():
    return render_template("index.html")

@views_bp.route("/areas")
def areas_page():
    return render_template("areas.html")

@views_bp.route("/empleados")
def empleados_page():
    return render_template("empleados.html")

@views_bp.route("/oficinas")
def oficinas_page():
    return render_template("oficinas.html")

@views_bp.route("/salones")
def salones_page():
    return render_template("salones.html")
