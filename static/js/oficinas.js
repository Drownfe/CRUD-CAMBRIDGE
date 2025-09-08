// ==========================
// CARGAR AREAS PARA SELECTS
// ==========================
async function cargarAreasSelect() {
    const res = await fetch("/api/areas");
    const areas = await res.json();

    const selectAdd = document.getElementById("idArea");
    const selectEdit = document.getElementById("editIdArea");

    [selectAdd, selectEdit].forEach(select => {
        select.innerHTML = '<option value="">Seleccione un Área</option>';
        areas.forEach(area => {
            const opt = document.createElement("option");
            opt.value = area.id;
            opt.textContent = area.nombre;
            select.appendChild(opt);
        });
    });
}

// ==========================
// CARGAR OFICINAS (READ)
// ==========================
async function cargarOficinas() {
    try {
        const res = await fetch("/api/oficinas");
        const oficinas = await res.json();

        const container = document.getElementById("oficinasContainer");
        container.innerHTML = "";

        oficinas.forEach(ofi => {
            const card = document.createElement("div");
            card.className = "col-lg-6 col-md-8 mb-3";
            card.innerHTML = `
                <div class="card custom-card">
                    <div class="card-header d-flex justify-content-between align-items-center">
                        <span><i class="fas fa-building"></i> ${ofi.codigo} <br>
                        <small>Área: ${ofi.areaNombre}</small></span>
                        <div>
                            <button class="btn btn-sm btn-warning me-2" onclick="editarOficina(${ofi.id}, '${ofi.codigo}', ${ofi.idArea})">
                                <i class="fas fa-edit"></i> Editar
                            </button>
                            <button class="btn btn-sm btn-danger" onclick="eliminarOficina(${ofi.id})">
                                <i class="fas fa-trash"></i> Eliminar
                            </button>
                        </div>
                    </div>
                </div>
            `;
            container.appendChild(card);
        });
    } catch (error) {
        console.error("Error al cargar oficinas:", error);
    }
}

// ==========================
// CREAR OFICINA (CREATE)
// ==========================
document.getElementById("formOficina").addEventListener("submit", async function(e) {
    e.preventDefault();

    const data = { 
        codigo: document.getElementById("codigo").value.trim(), 
        idArea: document.getElementById("idArea").value 
    };

    try {
        const response = await fetch("/api/oficinas", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        if (response.ok && result.status !== "error") {
            alert("Oficina agregada correctamente ✅");
            this.reset();
            cargarOficinas();
        } else {
            alert("⚠️ " + result.message);
        }
    } catch (error) {
        console.error("Error al crear oficina:", error);
    }
});

// ==========================
// EDITAR OFICINA (UPDATE)
// ==========================
function editarOficina(id, codigo, idArea) {
    document.getElementById("editIdOficina").value = id;
    document.getElementById("editCodigo").value = codigo;
    document.getElementById("editIdArea").value = idArea;

    new bootstrap.Modal(document.getElementById("modalEditarOficina")).show();
}

document.getElementById("formEditarOficina").addEventListener("submit", async function(e) {
    e.preventDefault();

    const id = document.getElementById("editIdOficina").value;
    const data = { 
        codigo: document.getElementById("editCodigo").value.trim(), 
        idArea: document.getElementById("editIdArea").value 
    };

    try {
        const response = await fetch(`/api/oficinas/${id}`, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        if (response.ok && result.status !== "error") {
            alert("Oficina actualizada correctamente ✅");
            bootstrap.Modal.getInstance(document.getElementById("modalEditarOficina")).hide();
            cargarOficinas();
        } else {
            alert("⚠️ " + result.message);
        }
    } catch (error) {
        console.error("Error al actualizar oficina:", error);
    }
});

// ==========================
// ELIMINAR OFICINA (DELETE)
// ==========================
async function eliminarOficina(id) {
    if (!confirm("¿Seguro que quieres eliminar esta oficina?")) return;

    try {
        const response = await fetch(`/api/oficinas/${id}`, { method: "DELETE" });
        const result = await response.json();

        if (response.ok && result.status !== "error") {
            alert("Oficina eliminada correctamente 🗑️");
            cargarOficinas();
        } else {
            alert("⚠️ " + result.message);
        }
    } catch (error) {
        console.error("Error al eliminar oficina:", error);
    }
}

// ==========================
// INICIALIZAR
// ==========================
document.addEventListener("DOMContentLoaded", () => {
    cargarAreasSelect();
    cargarOficinas();
});
