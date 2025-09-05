// ==========================
// CARGAR ÁREAS (READ)
// ==========================
async function cargarAreas() {
    try {
        const res = await fetch("/api/areas");
        const areas = await res.json();

        const container = document.getElementById("areasContainer");
        container.innerHTML = "";

        areas.forEach(area => {
            const card = document.createElement("div");
            card.className = "col-lg-6 col-md-8 mb-3";
            card.innerHTML = `
                <div class="card custom-card">
                    <div class="card-header d-flex justify-content-between align-items-center">
                        <span><i class="fas fa-landmark"></i> ${area.nombre} (ID: ${area.id})</span>
                        <div>
                            <button class="btn btn-sm btn-warning me-2" onclick="editarArea('${area.id}', '${area.nombre}')">
                                <i class="fas fa-edit"></i> Editar
                            </button>
                            <button class="btn btn-sm btn-danger" onclick="eliminarArea('${area.id}')">
                                <i class="fas fa-trash"></i> Eliminar
                            </button>
                        </div>
                    </div>
                </div>
            `;
            container.appendChild(card);
        });
    } catch (error) {
        console.error("Error al cargar áreas:", error);
    }
}

// CREAR ÁREA (POST /api/areas)
document.getElementById("formArea").addEventListener("submit", async function (e) {
    e.preventDefault();

    const data = { nombre: document.getElementById("nombre").value.trim() };

    try {
        const response = await fetch("/api/areas", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        if (response.ok && result.status === "ok") {
            alert(result.message);
            document.getElementById("formArea").reset();
            cargarAreas();
        } else {
            alert("⚠️ " + result.message);
        }
    } catch (error) {
        console.error("Error al crear área:", error);
        alert("❌ Error al crear el área");
    }
});


// ==========================
// EDITAR ÁREA (UPDATE)
// ==========================
function editarArea(id, nombre) {
    document.getElementById("editId").value = id;
    document.getElementById("editNombre").value = nombre;
    new bootstrap.Modal(document.getElementById("modalEditar")).show();
}

document.getElementById("formEditar").addEventListener("submit", async function (e) {
    e.preventDefault();

    const id = document.getElementById("editId").value;
    const data = { nombre: document.getElementById("editNombre").value.trim() };

    try {
        const response = await fetch(`/api/areas/${id}`, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data)
        });

        if (response.ok) {
            alert("Área actualizada correctamente ✅");
            bootstrap.Modal.getInstance(document.getElementById("modalEditar")).hide();
            cargarAreas();
        } else {
            alert("Error al actualizar el área ❌");
        }
    } catch (error) {
        console.error("Error al actualizar área:", error);
    }
});

// ELIMINAR ÁREA (DELETE /api/areas/:id)
async function eliminarArea(id) {
    if (!confirm("¿Seguro que quieres eliminar esta área?")) return;

    try {
        const response = await fetch(`/api/areas/${id}`, { method: "DELETE" });
        const result = await response.json();

        if (response.ok && result.status === "ok") {
            alert(result.message);
            cargarAreas();
        } else {
            alert("⚠️ " + result.message);
        }
    } catch (error) {
        console.error("Error al eliminar área:", error);
        alert("❌ Error al eliminar el área");
    }
}



// ==========================
// INICIALIZAR
// ==========================
document.addEventListener("DOMContentLoaded", cargarAreas);
