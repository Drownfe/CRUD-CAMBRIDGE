# 🎓 CRUD CAMBRIDGE – Proyecto Colegio 🚀

Este proyecto es una aplicación **Flask + MySQL** que implementa la gestión de la planta física y el personal de un colegio ficticio (Cambridge).  
Se desarrolló como parte de un taller académico de Tecnologías Web, cumpliendo con los requisitos solicitados: **arquitectura por capas, CRUD completo, reporte, diagrama de clases e informe**.

---

## ✨ Requisitos cumplidos
- ✔️ **Diagrama de clases** (realizado por el compañero de grupo).
- ✔️ **CRUD completo** para Áreas, Oficinas, Empleados y Salones.
- ✔️ **Reporte de Áreas y Empleados** (se puede generar desde la base de datos y visualizar en el sistema/informe).
- ✔️ **Informe final** (documento complementario con capturas y explicación del sistema).

---

## 📌 Funcionalidad
- **Áreas**: Se crean, editan y eliminan; un área contiene oficinas, empleados y salones.  
- **Oficinas**: Se asocian a un área, tienen un código único dentro de cada área.  
- **Empleados**: Se asocian a un área y oficina, tienen identificación única y clasificación (profesor planta/contratista o administrativo).  
- **Salones**: Se asocian a un área, con código único dentro de cada área.  

El sistema bloquea la eliminación si existen dependencias (ejemplo: no se puede borrar un área con oficinas o empleados asociados).

---

## 🛠️ Tecnologías utilizadas
- **Backend:** Flask, Flask-SQLAlchemy, Flask-CORS, PyMySQL, python-dotenv  
- **Frontend:** HTML5, Bootstrap 5, CSS personalizado, JavaScript (fetch API)  
- **Base de datos:** MySQL  
- **Entorno:** Python 3.13+  

---

## ⚙️ Instalación

1. Clonar el repositorio:
   ```bash
   git clone https://github.com/usuario/CRUD-CAMBRIDGE.git
   cd CRUD-CAMBRIDGE
   ```

2. Crear entorno virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate   # Linux/Mac
   venv\Scripts\activate    # Windows
   ```

3. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```

4. Configurar variables de entorno en `.env`:
   ```ini
   FLASK_APP=app.py
   FLASK_ENV=development
   SQLALCHEMY_DATABASE_URI=mysql+pymysql://usuario:password@localhost/cambridge_db
   SECRET_KEY=supersecreto
   ```

5. Crear base de datos en MySQL:
   ```sql
   CREATE DATABASE cambridge_db;
   ```

6. Ejecutar migraciones / crear tablas desde Python:
   ```bash
   flask shell
   >>> from models import db
   >>> db.create_all()
   ```

7. Cargar datos de ejemplo con el script SQL provisto o manualmente.  

8. Iniciar servidor:
   ```bash
   flask run
   ```

---

## 📂 Estructura del proyecto

```
CRUD-CAMBRIDGE/
│── app.py              # Punto de entrada principal
│── config.py           # Configuración (Flask, SQLAlchemy, CORS)
│── models.py           # Modelos de SQLAlchemy
│── requirements.txt    # Dependencias
│── .env                # Variables de entorno
│
├── routes/             # Blueprints (áreas, oficinas, empleados, salones, vistas)
├── templates/          # Plantillas HTML (index, áreas, oficinas, empleados, salones, reporte)
├── static/
│   ├── css/            # Estilos personalizados
│   └── js/             # Lógica frontend con fetch API
└── venv/               # Entorno virtual
```

---

## 🚀 Endpoints principales

### API REST
- **Áreas:** `/api/areas`
- **Oficinas:** `/api/oficinas`
- **Empleados:** `/api/empleados`
- **Salones:** `/api/salones`

### Vistas HTML
- `/` → Página principal (menú)  
- `/areas` → Gestión de Áreas  
- `/oficinas` → Gestión de Oficinas  
- `/empleados` → Gestión de Empleados  
- `/salones` → Gestión de Salones  
- `/reporte` → Reporte de Áreas y Empleados (capturas usadas en el informe final)  

---

## 🔒 Reglas de integridad implementadas

- `areas.nombre` → **único**  
- `empleados.identificacion` → **único**  
- `oficinas (codigo, id_area)` → **único por área**  
- `salones (codigo, id_area)` → **único por área**  
- **Restricciones de eliminación** → no se pueden borrar áreas, oficinas o salones si existen dependencias.  

---

## 👨‍💻 Autores
- **Juan Felipe Hernández** – Backend, frontend, base de datos.  
- **Compañera de grupo** – Diagrama de clases, informe final.  

Proyecto académico y personal de práctica con **Flask + MySQL + Frontend Web**.
