# 🎓 CRUD CAMBRIDGE - Proyecto Colegio 🚀

Aplicación web para la **gestión de Áreas, Empleados, Oficinas y Salones** de un colegio, construida con **Flask** + **MongoDB Atlas**.  

> ⚠️ Proyecto en construcción 🚧 — se siguen agregando módulos y funcionalidades.

---

## ✨ Características actuales

- 🐍 **Backend en Flask** conectado a MongoDB Atlas.  
- 📂 **Colecciones en la base de datos**:  
  - `areas`  
  - `empleados`  
  - `oficinas`  
  - `salones`  
- 🔗 **API REST** con rutas `GET`, `POST`, `PUT`, `DELETE`.  
- 🎨 **Frontend responsivo** con Bootstrap, mostrando datos en cards y tablas dinámicas.  
- 🔐 Conexión con GitHub lista (via SSH).  
- 📊 Datos de prueba realistas en MongoDB.

---

## 🛠️ Requisitos

- Python 3.8+  
- Cuenta en MongoDB Atlas (cluster configurado)  
- Virtualenv recomendado para aislar dependencias  

---

## ⚙️ Instalación y configuración

1. **Clona este repositorio**:

   ```bash
   git clone https://github.com/Drownfe/CRUD-CAMBRIDGE
   cd CRUD-CAMBRIDGE

2. **Crea y activa un entorno virtual:**:
    python -m venv venv
    # Linux/macOS
    source venv/bin/activate
    # Windows PowerShell
    venv\Scripts\activate
    
3. **Instala las dependencias:**:
    pip install Flask
    pip install pymongo

4. **Configura tu conexión a MongoDB Atlas en app.py, reemplazando la variable uri con tu string de conexión:**:
    uri = mongodb+srv://juanhernandez82161_db_user:3113700254@colegiocambridgecluster.trcaxho.mongodb.net/?retryWrites=true&w=majority&appName=ColegioCambridgeCluster"
5. **Verifica que exista la carpeta templates/ con las vistas HTML**:


▶️ Uso

Ejecuta la aplicación Flask: 
    python app.py

    Abre tu navegador en:

🌐 http://localhost:5000/areas
 → Listado de Áreas

👨‍🏫 http://localhost:5000/empleados
 → Listado de Empleados

🏢 http://localhost:5000/oficinas
 → Listado de Oficinas

🏫 http://localhost:5000/salones
 → Listado de Salones

También puedes probar los endpoints de la API REST:

GET /api/areas

POST /api/areas

PUT /api/areas/<id>

DELETE /api/areas/<id>

🚧 Estado del proyecto

✅ CRUD completo de Áreas (Create, Read, Update, Delete).
⏳ CRUD de Empleados, Oficinas y Salones en desarrollo.
🔐 Falta agregar autenticación y validaciones extra.

📬 Contacto

👤 Desarrollado por Juan Hernández
📧 Para dudas, sugerencias o colaboración → Abrir un issue en GitHub


