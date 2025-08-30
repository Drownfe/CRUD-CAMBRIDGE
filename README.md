# CRUD CAMBRIDGE - Proyecto Colegio

Este proyecto es una aplicación web para la gestión de áreas, empleados, oficinas y salones de un colegio pequeño, construida con Flask y MongoDB Atlas.

---

## Características actuales

- Backend con Flask conectado a MongoDB Atlas.
- Colecciones en la base de datos:  
  - `areas`  
  - `empleados`  
  - `oficinas`  
  - `salones`
- Rutas para consultar y crear datos (`GET` y `POST`).
- Páginas HTML estilizadas y responsivas usando Bootstrap para mostrar datos.
- Conexión SSH configurada para trabajar con GitHub.
- Contenido realista en base de datos para pruebas.

---

## Requisitos

- Python 3.8+  
- MongoDB Atlas (cuenta y base de datos configurada)  
- Dependencias Python instaladas (recomendado usar virtualenv)

---

## Instalación y configuración

1. Clona este repositorio:

git clone https://github.com/Drownfe/CRUD-CAMBRIDGE
cd CRUD-CAMBRIDGE


2. Crea y activa un entorno virtual:

python -m venv venv
source venv/bin/activate # Linux/macOS
venv\Scripts\activate # Windows PowerShell


3. Instala las dependencias:

pip install -r requirements.txt


4. Configura tu string de conexión MongoDB Atlas en `app.py` (reemplaza la variable `uri`):

uri = mongodb+srv://juanhernandez82161_db_user:3113700254@colegiocambridgecluster.trcaxho.mongodb.net/?retryWrites=true&w=majority&appName=ColegioCambridgeCluster"


5. Asegúrate de tener la carpeta `templates` con las plantillas HTML.

---

## Uso

1. Ejecuta la aplicación Flask:

python app.py

2. Abre el navegador y visita:

- http://localhost:5000/areas → Listado de áreas
- http://localhost:5000/empleados → Listado de empleados
- http://localhost:5000/oficinas → Listado de oficinas
- http://localhost:5000/salones → Listado de salones

3. Para crear nuevos registros usa los endpoints API REST:

- `POST /api/empleados`  
- `POST /api/oficinas`  
- `POST /api/salones`

con JSON en el body vía Postman o cliente HTTP.

---

## Importante

- Este proyecto está en desarrollo, falta implementar actualización, eliminación, autenticación y más validaciones.
- La configuración SSH permite subir repositorios a GitHub sin pedir usuario/contrasena siempre.

---

## Contacto

Para dudas o ayuda, contactar a Juan Hernández.


