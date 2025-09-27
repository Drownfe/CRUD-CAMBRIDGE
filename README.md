# 🏫 Colegio Cambridge - Sistema de Gestión Académica

Este proyecto implementa un sistema de gestión académica para el **Colegio Cambridge**, desarrollado en **Flask + MySQL** con dos capas de consumo:

- **CRUD clásico (REST/HTML)** para Áreas, Empleados, Oficinas y Salones.
- **GraphQL** con Ariadne para consultas y reportes avanzados.

---

## 🚀 Características

- CRUD completo de:
  - 📌 Áreas
  - 👩‍🏫 Empleados
  - 🏢 Oficinas
  - 🏫 Salones
- Reportes de Áreas con sus empleados (REST y GraphQL).
- Validaciones de integridad (no se eliminan áreas con dependencias, identificación única en empleados, etc.).
- Frontend responsivo con Bootstrap y cards modulares.
- Explorador **GraphiQL** en `/graphql`.

---

## ⚙️ Instalación

1. Clonar este repositorio:

   ```bash
   git clone <URL_REPOSITORIO>
   cd CRUD-CAMBRIDGE
   ```

2. Crear y activar entorno virtual:

   ```bash
   python -m venv venv
   source venv/bin/activate   # Linux/Mac
   venv\Scripts\activate    # Windows
   ```

3. Instalar dependencias:

   ```bash
   pip install -r requirements.txt
   ```

4. Configurar base de datos en `.env` o `config.py`:

   ```env
   DB_URI=mysql+pymysql://root:root1234@localhost/colegio_cambridge
   SECRET_KEY=supersecreto
   FLASK_DEBUG=1
   ```

5. Crear la base de datos e importar el esquema:

   ```sql
   CREATE DATABASE colegio_cambridge;
   USE colegio_cambridge;
   SOURCE schema.sql;
   SOURCE seed.sql;
   ```

6. Ejecutar el servidor:

   ```bash
   flask run
   ```

   La app estará disponible en [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## 📂 Estructura del proyecto

```
CRUD-CAMBRIDGE/
│── app.py
│── config.py
│── models.py
│── graphql_schema.py   # Definición de schema, queries, mutations, resolvers
│── requirements.txt
│── README.md
│
├── routes/             # Blueprints CRUD (áreas, empleados, oficinas, salones)
├── templates/          # HTML (Bootstrap)
│   └── index.html      # Home con cards y acceso a GraphQL
├── static/
│   ├── css/
│   │   ├── base.css
│   │   └── index.css
│   └── js/
│       └── index.js
└── venv/
```

---

## 🔗 Endpoints principales

- **Frontend CRUD clásico**
  - `/areas`
  - `/empleados`
  - `/oficinas`
  - `/salones`

- **API GraphQL**
  - `POST /graphql` → ejecutar queries y mutations
  - `GET /graphql` → interfaz GraphiQL para pruebas

---

## 🧩 Ejemplos GraphQL

### Listar áreas
```graphql
{
  areas {
    id
    nombre
  }
}
```

### Reporte de áreas con empleados
```graphql
{
  reporteAreasEmpleados {
    id
    nombre
    empleados {
      id
      nombre
      identificacion
    }
  }
}
```

### Crear área
```graphql
mutation {
  crearArea(data: { nombre: "Psicología" }) {
    id
    nombre
  }
}
```

### Crear empleado
```graphql
mutation {
  crearEmpleado(data: {
    identificacion: "999"
    nombre: "Sofía Ríos"
    tipo: "Profesor"
    subtipo: "Planta"
    idArea: 2
    idOficina: 3
  }) {
    id
    nombre
    identificacion
    area { nombre }
    oficina { codigo }
  }
}
```

### Editar empleado
```graphql
mutation {
  editarEmpleado(data: { id: 1, nombre: "Juan Pérez Gómez" }) {
    id
    nombre
  }
}
```

### Eliminar empleado
```graphql
mutation {
  eliminarEmpleado(id: 1)
}
```

---

## 📦 Dependencias principales

- Flask
- Flask-CORS
- Flask-SQLAlchemy
- PyMySQL
- python-dotenv
- Ariadne
- cryptography

Instalación:

```bash
pip install Flask Flask-CORS Flask-SQLAlchemy PyMySQL python-dotenv ariadne cryptography
```

---

## 🛠️ Errores comunes

- **Error 1045 Access denied** → Verificar usuario/clave en `DB_URI` y permisos en MySQL.
- **No database selected** → Asegurarse de ejecutar `USE colegio_cambridge;` antes de consultas SQL.
- **'cryptography' package is required** → Instalar con `pip install cryptography`.
- **405 Method Not Allowed en /graphql** → Usar `POST` o habilitar `GET` con GraphiQL (ya incluido).

---

## 📸 Evidencias sugeridas para entrega

- Captura de la home (`index.html`) con los 5 módulos (Áreas, Empleados, Oficinas, Salones, GraphQL).
- Capturas de GraphiQL ejecutando:
  - Query de áreas
  - Query de reporte áreas→empleados
  - Mutation de creación de empleado
- Captura del CRUD clásico mostrando el nuevo registro.

---

✨ Con este proyecto se cumple el taller y el parcial: CRUD clásico + capa GraphQL completa.
