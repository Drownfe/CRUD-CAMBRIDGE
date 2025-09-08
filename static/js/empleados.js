// ==========================
// CARGAR EMPLEADOS (READ)
// ==========================
async function cargarEmpleados() {
    try {
        const res = await fetch("/api/empleados");
        const empleados = await res.json();

        const container = document.getElementById("empleadosContainer");
        container.innerHTML = "";

        empleados.forEach(emp => {
            const card = document.createElement("div");
            card.className = "col-lg-6 col-md-8 mb-3";
            card.innerHTML = `
                <div class="card custom-card">
                    <div class="card-header d-flex justify-content-between align-items-center">
                        <span>
                            <i class="fas fa-user"></i> ${emp.nombre}  
                            <br><small>ID: ${emp.identificacion} | Tipo: ${emp.tipo || "-"} | Subtipo: ${emp.subtipo || "-"}</small>
                        </span>
                        <div>
                            <button class="btn btn-sm btn-warning me-2" onclick="editarEmpleado(${emp.id}, '${emp.identificacion}', '${emp.nombre}', '${emp.tipo || ""}', '${emp.subtipo || ""}')">
                                <i class="fas fa-edit"></i> Editar
                            </button>
                            <button class="btn btn-sm btn-danger" onclick="eliminarEmpleado(${emp.id})">
                                <i class="fas fa-trash"></i> Eliminar
                            </button>
                        </div>
                    </div>
                </div>
            `;
            container.appendChild(card);
        });
    } catch (error) {
        console.error("Error al cargar empleados:", error);
    }
}

// ==========================
// CREAR EMPLEADO (CREATE)
// ==========================
document.getElementById("formEmpleado").addEventListener("submit", async function(e) {
    e.preventDefault();

    const data = {
        identificacion: document.getElementById("identificacion").value.trim(),
        nombre: document.getElementById("nombre").value.trim(),
        tipo: document.getElementById("tipo").value.trim(),
        subtipo: document.getElementById("subtipo").value.trim(),
        idArea: 1,     // TODO: integrar selects de área
        idOficina: 1   // TODO: integrar selects de oficina
    };

    try {
        const response = await fetch("/api/empleados", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        if (response.ok && result.status !== "error") {
            alert("Empleado agregado correctamente ✅");
            this.reset();
            cargarEmpleados();
        } else {
            alert("⚠️ " + result.message);
        }
    } catch (error) {
        console.error("Error al crear empleado:", error);
    }
});

// ==========================
// EDITAR EMPLEADO (UPDATE)
// ==========================
function editarEmpleado(id, identificacion, nombre, tipo, subtipo) {
    document.getElementById("editIdEmpleado").value = id;
    document.getElementById("editIdentificacion").value = identificacion;
    document.getElementById("editNombre").value = nombre;
    document.getElementById("editTipo").value = tipo;
    document.getElementById("editSubtipo").value = subtipo;

    new bootstrap.Modal(document.getElementById("modalEditarEmpleado")).show();
}

document.getElementById("formEditarEmpleado").addEventListener("submit", async function(e) {
    e.preventDefault();

    const id = document.getElementById("editIdEmpleado").value;
    const data = {
        identificacion: document.getElementById("editIdentificacion").value.trim(),
        nombre: document.getElementById("editNombre").value.trim(),
        tipo: document.getElementById("editTipo").value.trim(),
        subtipo: document.getElementById("editSubtipo").value.trim(),
        idArea: 1,     // TODO: integrar selects de área
        idOficina: 1   // TODO: integrar selects de oficina
    };

    try {
        const response = await fetch(`/api/empleados/${id}`, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        if (response.ok && result.status !== "error") {
            alert("Empleado actualizado correctamente ✅");
            bootstrap.Modal.getInstance(document.getElementById("modalEditarEmpleado")).hide();
            cargarEmpleados();
        } else {
            alert("⚠️ " + result.message);
        }
    } catch (error) {
        console.error("Error al actualizar empleado:", error);
    }
});

// ==========================
// ELIMINAR EMPLEADO (DELETE)
// ==========================
async function eliminarEmpleado(id) {
    if (!confirm("¿Seguro que quieres eliminar este empleado?")) return;

    try {
        const response = await fetch(`/api/empleados/${id}`, { method: "DELETE" });
        const result = await response.json();

        if (response.ok && result.status !== "error") {
            alert("Empleado eliminado correctamente 🗑️");
            cargarEmpleados();
        } else {
            alert("⚠️ " + result.message);
        }
    } catch (error) {
        console.error("Error al eliminar empleado:", error);
    }
}

// ==========================
// INICIALIZAR
// ==========================
document.addEventListener("DOMContentLoaded", cargarEmpleados);
