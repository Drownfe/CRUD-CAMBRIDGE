from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os
from flask import Flask, render_template, request, jsonify, redirect, flash
from sqlalchemy.exc import IntegrityError

# ==============================================
# CONFIGURACIÓN DE FLASK
# ==============================================
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, "templates"),
    static_folder=os.path.join(BASE_DIR, "static")
)

CORS(app)

# ==============================================
# CONFIGURACIÓN DE MYSQL
# ==============================================

app.secret_key = "flash1234"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root1234@localhost/colegio_cambridge'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ==============================================
# MODELOS (Tablas)
# ==============================================

class Area(db.Model):
    __tablename__ = "areas"
    id_area = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100), unique=True, nullable=False)

    oficinas = db.relationship("Oficina", backref="area", cascade="all, delete", passive_deletes=True)
    empleados = db.relationship("Empleado", backref="area", cascade="all, delete", passive_deletes=True)
    salones = db.relationship("Salon", backref="area", cascade="all, delete", passive_deletes=True)

    def to_dict(self):
        return {"id": self.id_area, "nombre": self.nombre}
class Oficina(db.Model):
    __tablename__ = "oficinas"
    id_oficina = db.Column(db.Integer, primary_key=True, autoincrement=True)
    codigo = db.Column(db.String(100), unique=True, nullable=False)
    id_area = db.Column(db.Integer, db.ForeignKey("areas.id_area", ondelete="RESTRICT"), nullable=False)

    empleados = db.relationship("Empleado", backref="oficina", cascade="all, delete", passive_deletes=True)

    def to_dict(self):
        return {"id": self.id_oficina, "codigo": self.codigo, "idArea": self.id_area}
class Empleado(db.Model):
    __tablename__ = "empleados"
    id_empleado = db.Column(db.Integer, primary_key=True, autoincrement=True)
    identificacion = db.Column(db.String(50), nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    tipo = db.Column(db.String(50))
    subtipo = db.Column(db.String(50))
    id_area = db.Column(db.Integer, db.ForeignKey("areas.id_area", ondelete="RESTRICT"), nullable=False)
    id_oficina = db.Column(db.Integer, db.ForeignKey("oficinas.id_oficina", ondelete="RESTRICT"), nullable=False)

    def to_dict(self):
        return {
            "id": self.id_empleado,
            "identificacion": self.identificacion,
            "nombre": self.nombre,
            "tipo": self.tipo,
            "subtipo": self.subtipo,
            "idArea": self.id_area,
            "idOficina": self.id_oficina
        }
class Salon(db.Model):
    __tablename__ = "salones"
    id_salon = db.Column(db.Integer, primary_key=True, autoincrement=True)
    codigo = db.Column(db.String(100), unique=True, nullable=False)
    id_area = db.Column(db.Integer, db.ForeignKey("areas.id_area", ondelete="RESTRICT"), nullable=False)

    def to_dict(self):
        return {"id": self.id_salon, "codigo": self.codigo, "idArea": self.id_area}

# ==============================================
# RUTAS HTML
# ==============================================

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/areas")
def areas():
    all_areas = Area.query.order_by(Area.id_area.asc()).all()
    return render_template("Areas/areas.html", areas=all_areas)

@app.route("/areas/edit/<int:id>", methods=["GET", "POST"])
def edit_area(id):
    area = Area.query.get_or_404(id)
    if request.method == "POST":
        nuevo_nombre = request.form["nombre"].strip().title()

        # Validación de longitud
        if len(nuevo_nombre) < 3 or len(nuevo_nombre) > 100:
            flash("⚠️ El nombre del área debe tener entre 3 y 100 caracteres.", "warning")
            return redirect(f"/areas/edit/{id}")

        # Validación de unicidad (ignora el área actual)
        existente = Area.query.filter(
            Area.nombre.ilike(nuevo_nombre),
            Area.id_area != id
        ).first()
        if existente:
            flash("⚠️ Ya existe otra área con ese nombre.", "danger")
            return redirect(f"/areas/edit/{id}")

        area.nombre = nuevo_nombre
        db.session.commit()
        flash("Área actualizada con éxito ✅", "success")
        return redirect("/areas")

    return render_template("Areas/edit_areas.html", area=area)

@app.route("/empleados")
def empleados_page():
    return render_template("empleados.html")

@app.route("/oficinas")
def oficinas_page():
    return render_template("oficinas.html")

@app.route("/salones")
def salones_page():
    return render_template("salones.html")

# ==============================================
# API AREAS
# ==============================================

@app.route("/api/areas", methods=["GET"])
def get_areas():
    areas = Area.query.all()
    return jsonify([a.to_dict() for a in areas])

@app.route("/areas/add", methods=["POST"])
def add_area():
    nombre = request.form["nombre"].strip().title()

    # Validación de longitud
    if len(nombre) < 3 or len(nombre) > 100:
        flash("⚠️ El nombre del área debe tener entre 3 y 100 caracteres.", "warning")
        return redirect("/areas")

    # Validación de unicidad
    existente = Area.query.filter(Area.nombre.ilike(nombre)).first()
    if existente:
        flash("⚠️ El área ya existe, ingresa un nombre diferente.", "danger")
        return redirect("/areas")

    nueva_area = Area(nombre=nombre)
    db.session.add(nueva_area)
    db.session.commit()
    flash("Área agregada con éxito ✅", "success")
    return redirect("/areas")

@app.route("/api/areas/<int:id>", methods=["PUT"])
def update_area(id):
    area = Area.query.get_or_404(id)
    data = request.json
    area.nombre = data.get("nombre", area.nombre)
    db.session.commit()
    return jsonify(area.to_dict())

@app.route("/areas/delete/<int:id>")
def delete_area(id):
    area = Area.query.get_or_404(id)
    try:
        db.session.delete(area)
        db.session.commit()
        flash("Área eliminada con éxito 🗑️", "success")
    except IntegrityError:
        db.session.rollback()  # Deshace la transacción
        flash("⚠️ No se puede eliminar el área porque tiene oficinas, empleados o salones asociados.", "danger")
    return redirect("/areas")

# ==============================================
# API OFICINAS
# ==============================================

@app.route("/api/oficinas", methods=["GET"])
def get_oficinas():
    oficinas = Oficina.query.all()
    return jsonify([o.to_dict() for o in oficinas])

@app.route("/api/oficinas", methods=["POST"])
def add_oficina():
    data = request.json
    nueva_oficina = Oficina(codigo=data["codigo"], id_area=data["idArea"])
    db.session.add(nueva_oficina)
    db.session.commit()
    return jsonify(nueva_oficina.to_dict()), 201

@app.route("/api/oficinas/<int:id>", methods=["PUT"])
def update_oficina(id):
    oficina = Oficina.query.get_or_404(id)
    data = request.json
    oficina.codigo = data.get("codigo", oficina.codigo)
    oficina.id_area = data.get("idArea", oficina.id_area)
    db.session.commit()
    return jsonify(oficina.to_dict())

@app.route("/api/oficinas/<int:id>", methods=["DELETE"])
def delete_oficina(id):
    oficina = Oficina.query.get_or_404(id)
    db.session.delete(oficina)
    db.session.commit()
    return jsonify({"message": "Oficina eliminada"})

# ==============================================
# API EMPLEADOS
# ==============================================
@app.route("/api/empleados", methods=["GET"])
def get_empleados():
    empleados = Empleado.query.all()
    return jsonify([e.to_dict() for e in empleados])

@app.route("/api/empleados", methods=["POST"])
def add_empleado():
    data = request.json
    nuevo_empleado = Empleado(
        identificacion=data["identificacion"],
        nombre=data["nombre"],
        tipo=data.get("tipo"),
        subtipo=data.get("subtipo"),
        id_area=data["idArea"],
        id_oficina=data["idOficina"]
    )
    db.session.add(nuevo_empleado)
    db.session.commit()
    return jsonify(nuevo_empleado.to_dict()), 201

@app.route("/api/empleados/<int:id>", methods=["PUT"])
def update_empleado(id):
    empleado = Empleado.query.get_or_404(id)
    data = request.json
    empleado.identificacion = data.get("identificacion", empleado.identificacion)
    empleado.nombre = data.get("nombre", empleado.nombre)
    empleado.tipo = data.get("tipo", empleado.tipo)
    empleado.subtipo = data.get("subtipo", empleado.subtipo)
    empleado.id_area = data.get("idArea", empleado.id_area)
    empleado.id_oficina = data.get("idOficina", empleado.id_oficina)
    db.session.commit()
    return jsonify(empleado.to_dict())

@app.route("/api/empleados/<int:id>", methods=["DELETE"])
def delete_empleado(id):
    empleado = Empleado.query.get_or_404(id)
    db.session.delete(empleado)
    db.session.commit()
    return jsonify({"message": "Empleado eliminado"})


# ==============================================
# API SALONES
# ==============================================
@app.route("/api/salones", methods=["GET"])
def get_salones():
    salones = Salon.query.all()
    return jsonify([s.to_dict() for s in salones])

@app.route("/api/salones", methods=["POST"])
def add_salon():
    data = request.json
    nuevo_salon = Salon(codigo=data["codigo"], id_area=data["idArea"])
    db.session.add(nuevo_salon)
    db.session.commit()
    return jsonify(nuevo_salon.to_dict()), 201

@app.route("/api/salones/<int:id>", methods=["PUT"])
def update_salon(id):
    salon = Salon.query.get_or_404(id)
    data = request.json
    salon.codigo = data.get("codigo", salon.codigo)
    salon.id_area = data.get("idArea", salon.id_area)
    db.session.commit()
    return jsonify(salon.to_dict())

@app.route("/api/salones/<int:id>", methods=["DELETE"])
def delete_salon(id):
    salon = Salon.query.get_or_404(id)
    db.session.delete(salon)
    db.session.commit()
    return jsonify({"message": "Salón eliminado"})


# ==============================================
# MAIN
# ==============================================
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)