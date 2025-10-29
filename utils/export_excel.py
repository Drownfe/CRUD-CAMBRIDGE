# utils/export_excel.py
import os
from datetime import datetime
import pandas as pd
from flask import current_app, url_for

from models import Area, Oficina, Empleado, Salon

def _exports_dir():
    os.makedirs(os.path.join(current_app.static_folder, "exports"), exist_ok=True)
    return os.path.join(current_app.static_folder, "exports")

def _timestamp():
    return datetime.now().strftime("%Y%m%d_%H%M%S")

def export_areas_xlsx():
    rows = [{"ID": a.id_area, "Nombre": a.nombre} for a in Area.query.order_by(Area.id_area).all()]
    filename = f"areas_{_timestamp()}.xlsx"
    path = os.path.join(_exports_dir(), filename)
    pd.DataFrame(rows).to_excel(path, index=False, engine="openpyxl")
    return url_for("static", filename=f"exports/{filename}", _external=True)

def export_oficinas_xlsx():
    rows = [{"ID": o.id_oficina, "Código": o.codigo, "ID Área": o.id_area} for o in Oficina.query.order_by(Oficina.id_oficina).all()]
    filename = f"oficinas_{_timestamp()}.xlsx"
    path = os.path.join(_exports_dir(), filename)
    pd.DataFrame(rows).to_excel(path, index=False, engine="openpyxl")
    return url_for("static", filename=f"exports/{filename}", _external=True)

def export_empleados_xlsx():
    rows = [{
        "ID": e.id_empleado,
        "Identificación": e.identificacion,
        "Nombre": e.nombre,
        "Tipo": e.tipo,
        "Subtipo": e.subtipo or "",
        "ID Área": e.id_area,
        "ID Oficina": e.id_oficina,
    } for e in Empleado.query.order_by(Empleado.id_empleado).all()]
    filename = f"empleados_{_timestamp()}.xlsx"
    path = os.path.join(_exports_dir(), filename)
    pd.DataFrame(rows).to_excel(path, index=False, engine="openpyxl")
    return url_for("static", filename=f"exports/{filename}", _external=True)

def export_salones_xlsx():
    rows = [{
        "ID": s.id_salon,
        "Código/No": s.codigo,
        "Capacidad": getattr(s, "capacidad", None),
        "ID Área": s.id_area,
    } for s in Salon.query.order_by(Salon.id_salon).all()]
    filename = f"salones_{_timestamp()}.xlsx"
    path = os.path.join(_exports_dir(), filename)
    pd.DataFrame(rows).to_excel(path, index=False, engine="openpyxl")
    return url_for("static", filename=f"exports/{filename}", _external=True)

def export_reporte_general_xlsx():
    """
    Genera un Excel con todas las tablas (áreas, oficinas, salones, empleados)
    en diferentes hojas dentro del mismo archivo.
    """
    os.makedirs(os.path.join(current_app.static_folder, "exports"), exist_ok=True)
    filename = f"reporte_general_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    path = os.path.join(current_app.static_folder, "exports", filename)

    # Crear writer con múltiples hojas
    with pd.ExcelWriter(path, engine="openpyxl") as writer:
        # Áreas
        areas = [{"ID": a.id_area, "Nombre": a.nombre} for a in Area.query.order_by(Area.nombre).all()]
        pd.DataFrame(areas).to_excel(writer, index=False, sheet_name="Áreas")

        # Oficinas
        oficinas = [{
            "ID": o.id_oficina,
            "Código": o.codigo,
            "Área": o.area.nombre if o.area else None
        } for o in Oficina.query.order_by(Oficina.codigo).all()]
        pd.DataFrame(oficinas).to_excel(writer, index=False, sheet_name="Oficinas")

        # Salones
        salones = [{
            "ID": s.id_salon,
            "Código": s.codigo,
            "Capacidad": s.capacidad,
            "Área": s.area.nombre if s.area else None
        } for s in Salon.query.order_by(Salon.codigo).all()]
        pd.DataFrame(salones).to_excel(writer, index=False, sheet_name="Salones")

        # Empleados
        empleados = [{
            "ID": e.id_empleado,
            "Identificación": e.identificacion,
            "Nombre": e.nombre,
            "Tipo": e.tipo,
            "Subtipo": e.subtipo or "",
            "Área": e.area.nombre if e.area else None,
            "Oficina": e.oficina.codigo if e.oficina else None
        } for e in Empleado.query.order_by(Empleado.nombre).all()]
        pd.DataFrame(empleados).to_excel(writer, index=False, sheet_name="Empleados")

    return url_for("static", filename=f"exports/{filename}", _external=True)
