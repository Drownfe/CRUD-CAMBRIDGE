# 🏫 Colegio Cambridge - Sistema de Gestión Académica

Este proyecto implementa un sistema de gestión académica para el **Colegio Cambridge**, desarrollado en **Flask + MySQL**, con doble capa de acceso a los datos:

- **CRUD clásico (REST/HTML)** para Áreas, Empleados, Oficinas y Salones.  
- **GraphQL (Ariadne)** para consultas, mutaciones y generación automática de reportes en Excel.

---

## 🚀 Características principales

- CRUD completo para:
  - 📌 Áreas  
  - 👩‍🏫 Empleados  
  - 🏢 Oficinas  
  - 🏫 Salones  
- Validaciones de integridad (no eliminar registros con dependencias, campos únicos, etc.).  
- Reporte combinado de áreas con sus empleados.  
- **Exportación automática a Excel** cada vez que se ejecuta una mutation en GraphQL.  
- Interfaz GraphiQL incorporada en `/graphql` para pruebas directas.  
- Frontend con Bootstrap y tarjetas modulares (incluye botón ⚡ para GraphQL).

---

## ⚙️ Instalación y configuración

1. Clonar el repositorio  
   ```bash
   git clone <URL_REPOSITORIO>
   cd CRUD-CAMBRIDGE
   ```

2. Crear entorno virtual e instalar dependencias  
   ```bash
   python -m venv venv
   venv\Scripts\activate   # Windows
   pip install -r requirements.txt
   ```

3. Configurar conexión a base de datos (`.env` o `config.py`)  
   ```env
   DB_URI=mysql+pymysql://root:root1234@localhost/colegio_cambridge
   SECRET_KEY=supersecreto
   FLASK_DEBUG=1
   ```

4. Crear la base de datos y tablas  
   ```sql
   SOURCE schema.sql;
   SOURCE seed.sql;
   ```

5. Ejecutar la app  
   ```bash
   flask run
   ```

---

## 📂 Estructura del proyecto

```
CRUD-CAMBRIDGE/
│── app.py
│── config.py
│── models.py
│── graphql_schema.py
│── requirements.txt
│── README.md
│
├── routes/
│   ├── areas.py
│   ├── empleados.py
│   ├── oficinas.py
│   └── salones.py
│
├── utils/
│   └── export_excel.py   # generación automática de Excel
│
├── static/
│   ├── css/
│   ├── js/
│   └── exports/          # se guardan los Excel generados aquí
└── templates/
    └── index.html
```

---

## 🔗 Endpoints principales

| Tipo | Ruta | Descripción |
|------|------|--------------|
| Frontend | `/` | Página principal con módulos |
| CRUD REST | `/areas`, `/empleados`, `/oficinas`, `/salones` | Interfaces HTML |
| GraphQL API | `/graphql` | Endpoint para queries y mutations |
| Descargas | `/static/exports/...` | Archivos Excel generados automáticamente |

---

## 🧩 Ejemplos GraphQL con exportación automática

Cada mutation genera un archivo Excel actualizado en `static/exports/`  
y devuelve la URL (`exportUrl`) en la respuesta.

---

### 🔹 ÁREAS

#### 🟩 Crear área de prueba
```graphql
mutation {
  crearArea(data: { nombre: "Psicología Experimental" }) {
    ok
    message
    exportUrl
    area { id nombre }
  }
}
```

#### 🟨 Editar área
```graphql
mutation {
  editarArea(data: { id: 5, nombre: "Psicología Aplicada" }) {
    ok
    message
    exportUrl
    area { id nombre }
  }
}
```

#### 🟥 Eliminar área
```graphql
mutation {
  eliminarArea(id: 5) {
    ok
    message
    exportUrl
  }
}
```

---

### 🔹 EMPLEADOS

#### 🟩 Crear empleado de prueba
```graphql
mutation {
  crearEmpleado(
    data: {
      identificacion: "TEST001"
      nombre: "Laura Restrepo"
      tipo: "Profesor"
      subtipo: "Psicología"
      idArea: 2
      idOficina: 3
    }
  ) {
    ok
    message
    exportUrl
    empleado {
      id
      nombre
      identificacion
      area { nombre }
      oficina { codigo }
    }
  }
}
```

#### 🟨 Editar empleado
```graphql
mutation {
  editarEmpleado(
    data: {
      id: 9
      nombre: "Laura Restrepo Vargas"
      subtipo: "Psicología Experimental"
    }
  ) {
    ok
    message
    exportUrl
    empleado { id nombre subtipo }
  }
}
```

#### 🟥 Eliminar empleado
```graphql
mutation {
  eliminarEmpleado(id: 9) {
    ok
    message
    exportUrl
  }
}
```

---

## 📦 Dependencias principales

```
Flask
Flask-Cors
Flask-SQLAlchemy
PyMySQL
python-dotenv
ariadne
cryptography
pandas
openpyxl
```

---

## 🧠 Errores comunes

| Error | Causa | Solución |
|-------|--------|-----------|
| `(1045) Access denied` | Usuario o clave de MySQL incorrectos | Revisar `DB_URI` y permisos |
| `No database selected` | No se ejecutó `USE colegio_cambridge` | Crear base o actualizar URI |
| `cryptography required` | Falta paquete para MySQL 8 | `pip install cryptography` |
| `405 Method Not Allowed` | GraphQL acepta solo POST | Usa método POST o abre UI GET `/graphql` |

---

## 📸 Evidencias sugeridas para la entrega

1. Captura de la **página principal** con el nuevo botón ⚡ GraphQL.  
2. Capturas en **GraphiQL** ejecutando:
   - Crear / Editar / Eliminar área.
   - Crear / Editar / Eliminar empleado.
3. Captura mostrando el **Excel descargado automáticamente** tras la mutation.
4. Captura del **CRUD clásico** mostrando el nuevo registro.

---

## ✨ Conclusión

El proyecto cumple completamente con el taller y parcial:
- CRUD clásico funcional.  
- Capa GraphQL con queries, mutations y reporte áreas→empleados.  
- Generación automática de reportes Excel tras cada modificación.  
- Interfaz unificada y pruebas evidentes para documentación.  
