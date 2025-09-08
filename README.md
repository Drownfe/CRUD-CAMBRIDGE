# 🎓 CRUD CAMBRIDGE - Proyecto Colegio 🚀

Aplicación web para la **gestión de Áreas, Empleados, Oficinas y Salones** del Colegio Cambridge.  
Construida con **Flask + SQLAlchemy + MySQL**, integrando un modelo **relacional** con rutas CRUD completas, frontend en **HTML + Bootstrap + CSS + JavaScript**, y estructura modular con **Blueprints**.

> ⚠️ Proyecto en construcción 🚧 — se siguen agregando módulos y funcionalidades.

---

## ✨ Características actuales

- 🐍 **Backend en Flask** conectado a MySQL mediante SQLAlchemy.  
- 📂 **Tablas en la base de datos**:  
  - `areas`  
  - `empleados`  
  - `oficinas`  
  - `salones`  
- 🔗 **API REST** modularizada con `Blueprints` y rutas `/api/...`.  
- 🎨 **Frontend responsivo** con Bootstrap, CSS propios y JS dinámico por módulo.  
- 🛡️ **Reglas implementadas**:  
  - Áreas:  
    - No se pueden duplicar nombres.  
    - Nombre entre 3 y 100 caracteres.  
    - No se pueden eliminar si tienen oficinas, empleados o salones asociados.  
  - Empleados:  
    - Identificación obligatoria y única.  
    - Nombre mínimo 3 caracteres.  
    - Deben estar vinculados a un área y a una oficina existente.  
  - Oficinas:  
    - Código obligatorio y único.  
    - Longitud entre 2 y 100 caracteres.  
    - Deben pertenecer a un área existente.  
    - No se pueden eliminar si tienen empleados asociados.  
  - Salones:  
    - Código obligatorio y único.  
    - Longitud entre 2 y 50 caracteres.  
    - Deben pertenecer a un área existente.  

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

   Dependencias principales:
   - Flask  
   - Flask-SQLAlchemy  
   - Flask-CORS  
   - PyMySQL  
   - python-dotenv  

4. **Configura la base de datos MySQL**:

   - Entra a la consola de MySQL:

     ```bash
     mysql -u root -p
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
   - 🌐 [http://localhost:5000/areas](http://localhost:5000/areas) → Áreas del Colegio  
   - 👨‍🏫 [http://localhost:5000/empleados](http://localhost:5000/empleados) → Empleados  
   - 🏢 [http://localhost:5000/oficinas](http://localhost:5000/oficinas) → Oficinas  
   - 🏫 [http://localhost:5000/salones](http://localhost:5000/salones) → Salones  

---

## 📂 Estructura del proyecto

```
PDYP_CAMBRIDGE/
│── app.py
│── config.py
│── models.py
│── .env
│── requirements.txt
│
├── routes/
│   ├── areas.py
│   ├── empleados.py
│   ├── oficinas.py
│   ├── salones.py
│   └── views.py
│
├── templates/
│   ├── index.html
│   │
│   ├── Areas/
│   │   └── areas.html
│   │
│   ├── Empleados/
│   │   └── empleados.html
│   │
│   ├── Oficinas/
│   │   └── oficinas.html
│   │
│   └── Salones/
│       └── salones.html
│
├── static/
│   ├── css/
│   │   ├── areas.css
│   │   ├── empleados.css
│   │   ├── oficinas.css
│   │   └── salones.css
│   │
│   └── js/
│       ├── areas.js
│       ├── empleados.js
│       ├── oficinas.js
│       └── salones.js
│
└── README.md
```

---

## 🚧 Estado del proyecto

✅ Migración completa a **estructura modular con Blueprints**.  
✅ CRUD de **Áreas, Empleados, Oficinas y Salones** operativos.  
✅ Validaciones y reglas de negocio implementadas.  
⏳ Pendiente: mejoras visuales y validaciones adicionales en frontend.  

---

## 📬 Contacto

👤 Desarrollado por **Juan Hernández**  
📧 Para dudas, sugerencias o colaboración → [Abrir un issue en GitHub](https://github.com/Drownfe/CRUD-CAMBRIDGE/issues)
