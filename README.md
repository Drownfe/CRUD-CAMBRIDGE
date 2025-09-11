# 🎓 CRUD CAMBRIDGE – Proyecto Colegio 🚀

Este proyecto es una aplicación **Flask + MySQL** para la gestión de un colegio ficticio (Cambridge).  
Permite administrar **Áreas, Oficinas, Empleados y Salones** a través de un sistema CRUD con interfaz web.

---

## ✨ Características
- CRUD completo para:
  - Áreas (con validación de unicidad y dependencias)
  - Oficinas (asociadas a un Área)
  - Empleados (asociados a un Área y Oficina)
  - Salones (asociados a un Área)
- Validaciones de datos en backend y frontend
- Bloqueo de eliminación cuando existen dependencias (IntegrityError controlado)
- Interfaz web con **Bootstrap + CSS personalizado**
- Rutas API REST (`/api/...`) + Rutas HTML (`/...`)
- Configuración con variables de entorno (`.env`)

---

## 🛠️ Tecnologías
- **Backend:** Flask, Flask-SQLAlchemy, Flask-CORS, PyMySQL, python-dotenv
- **Frontend:** HTML + Bootstrap 5, CSS, JavaScript (fetch API)
- **Base de datos:** MySQL
- **Entorno:** Python 3.13+

---

## ⚙️ Instalación

1. Clonar repositorio:
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

6. Inicializar tablas:
   ```bash
   flask shell
   >>> from models import db
   >>> db.create_all()
   ```

7. Ejecutar servidor:
   ```bash
   flask run
   ```

---

## 📂 Estructura del proyecto

```
CRUD-CAMBRIDGE/
│── app.py              # Punto de entrada principal
│── config.py           # Configuración (MySQL, Flask, CORS)
│── models.py           # Modelos de SQLAlchemy
│── requirements.txt    # Dependencias
│── .env                # Variables de entorno
│
├── routes/             # Blueprints (Áreas, Oficinas, Empleados, Salones, Views)
├── templates/          # Plantillas HTML (index, áreas, oficinas, empleados, salones)
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
- `/` → Página principal
- `/areas` → Gestión de Áreas
- `/oficinas` → Gestión de Oficinas
- `/empleados` → Gestión de Empleados
- `/salones` → Gestión de Salones

---

## 👨‍💻 Autor
Desarrollado por **Juan Felipe Hernández**  
Proyecto académico y personal para práctica de **Flask + MySQL + Frontend**.
