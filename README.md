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
   ```

2. **Crea y activa un entorno virtual**:

   ```bash
   python -m venv venv
   # Linux/macOS
   source venv/bin/activate
   # Windows PowerShell
   venv\Scripts\activate
   ```

3. **Instala las dependencias**:

   👉 Si tienes `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```

   👉 O instálalas manualmente:
   ```bash
   pip install Flask
   pip install pymongo
   ```

4. **Configura tu conexión a MongoDB Atlas** en `app.py`, reemplazando la variable `uri` con tu string de conexión:

   ```python
   uri = "mongodb+srv://<usuario>:<contraseña>@colegiocambridgecluster.xxxxx.mongodb.net/?retryWrites=true&w=majority"
   ```

5. Verifica que exista la carpeta `templates/` con las vistas HTML.  

---

## ▶️ Uso

1. **Ejecuta la aplicación Flask**:

   ```bash
   python app.py
   ```

2. Abre tu navegador en:  
   - 🌐 [http://localhost:5000/areas](http://localhost:5000/areas) → Listado de Áreas  
   - 👨‍🏫 [http://localhost:5000/empleados](http://localhost:5000/empleados) → Listado de Empleados  
   - 🏢 [http://localhost:5000/oficinas](http://localhost:5000/oficinas) → Listado de Oficinas  
   - 🏫 [http://localhost:5000/salones](http://localhost:5000/salones) → Listado de Salones  

3. También puedes probar los endpoints de la API REST:  
   - `GET /api/areas`  
   - `POST /api/areas`  
   - `PUT /api/areas/<id>`  
   - `DELETE /api/areas/<id>`  

---

## 🚧 Estado del proyecto

✅ CRUD completo de **Áreas** (Create, Read, Update, Delete).  
⏳ CRUD de **Empleados, Oficinas y Salones** en desarrollo.  
🔐 Falta agregar autenticación y validaciones extra.  

---

## 📬 Contacto

👤 Desarrollado por **Juan Hernández**  
📧 Para dudas, sugerencias o colaboración → [Abrir un issue en GitHub](https://github.com/Drownfe/CRUD-CAMBRIDGE/issues)  
