# 🎓 CRUD CAMBRIDGE - Proyecto Colegio 🚀

Aplicación web para la **gestión de Áreas, Empleados, Oficinas y Salones** del Colegio Cambridge.  
Construida con **Flask + SQLAlchemy + MySQL**, integrando un modelo **relacional** con rutas CRUD completas y frontend en **HTML + Bootstrap + CSS**.

> ⚠️ Proyecto en construcción 🚧 — se siguen agregando módulos y funcionalidades.

---

## ✨ Características actuales

- 🐍 **Backend en Flask** conectado a MySQL mediante SQLAlchemy.  
- 📂 **Tablas en la base de datos**:  
  - `areas`  
  - `empleados`  
  - `oficinas`  
  - `salones`  
- 🔗 **API REST** con rutas `GET`, `POST`, `PUT`, `DELETE`.  
- 🎨 **Frontend responsivo** con Bootstrap y estilos propios en `static/css/styles.css`.  
- 🔐 Modelo relacional con claves foráneas para asegurar integridad.  

---

## 🛠️ Requisitos

- Python 3.10+  
- MySQL Server 8+  
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

   ```bash
   pip install -r requirements.txt
   ```

   Si necesitas instalarlas manualmente:

   ```bash
   pip install flask flask_sqlalchemy pymysql python-dotenv
   ```

4. **Configura la base de datos MySQL**:

   - Entra a la consola de MySQL:

     ```bash
     mysql -u root -p
     ```

   - Cambia la autenticación de root (si es necesario):

     ```sql
     ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'root1234';
     FLUSH PRIVILEGES;
     ```

   - Crea la base de datos:

     ```sql
     CREATE DATABASE colegio_cambridge;
     ```

5. **Configura el archivo `.env`** en la raíz del proyecto:

   ```
   DB_URI=mysql+pymysql://root:root1234@localhost/colegio_cambridge
   ```

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

✅ Migración completa de **MongoDB a MySQL relacional**.  
✅ CRUD de **Áreas** operativo.  
✅ CRUD de **Empleados, Oficinas y Salones** en desarrollo.  
⏳ Pendiente agregar autenticación y validaciones extra.  

---

## 📬 Contacto

👤 Desarrollado por **Juan Hernández**  
📧 Para dudas, sugerencias o colaboración → [Abrir un issue en GitHub](https://github.com/Drownfe/CRUD-CAMBRIDGE/issues)  
