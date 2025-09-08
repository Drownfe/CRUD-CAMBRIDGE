from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# ==============================================
# MODELOS (Tablas)
# ==============================================

class Area(db.Model):
    __tablename__ = "areas"
    id_area = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100), unique=True, nullable=False)

    # Relaciones
    oficinas = db.relationship("Oficina", backref="area", cascade="all, delete", passive_deletes=True)
    empleados = db.relationship("Empleado", backref="area", cascade="all, delete", passive_deletes=True)
    salones = db.relationship("Salon", backref="area", cascade="all, delete", passive_deletes=True)

    def to_dict(self):
        return {
            "id": self.id_area,
            "nombre": self.nombre
        }


class Oficina(db.Model):
    __tablename__ = "oficinas"
    id_oficina = db.Column(db.Integer, primary_key=True, autoincrement=True)
    codigo = db.Column(db.String(100), unique=True, nullable=False)
    id_area = db.Column(db.Integer, db.ForeignKey("areas.id_area", ondelete="RESTRICT"), nullable=False)

    # Relaciones
    empleados = db.relationship("Empleado", backref="oficina", cascade="all, delete", passive_deletes=True)

    def to_dict(self):
        return {
            "id": self.id_oficina,
            "codigo": self.codigo,
            "idArea": self.id_area,
            "areaNombre": self.area.nombre if self.area else None
        }


class Empleado(db.Model):
    __tablename__ = "empleados"
    id_empleado = db.Column(db.Integer, primary_key=True, autoincrement=True)
    identificacion = db.Column(db.String(50), unique=True, nullable=False)
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
            "areaNombre": self.area.nombre if self.area else None,
            "idOficina": self.id_oficina,
            "oficinaCodigo": self.oficina.codigo if self.oficina else None
        }


class Salon(db.Model):
    __tablename__ = "salones"
    id_salon = db.Column(db.Integer, primary_key=True, autoincrement=True)
    codigo = db.Column(db.String(100), unique=True, nullable=False)
    id_area = db.Column(db.Integer, db.ForeignKey("areas.id_area", ondelete="RESTRICT"), nullable=False)

    def to_dict(self):
        return {
            "id": self.id_salon,
            "codigo": self.codigo,
            "idArea": self.id_area,
            "areaNombre": self.area.nombre if self.area else None
        }
