document.addEventListener("DOMContentLoaded", () => {
  const formArea = document.getElementById("formArea");
  const nombreInput = document.getElementById("nombreArea");
  const listaAreas = document.getElementById("listaAreas");

  // 🔹 Cargar las áreas al inicio
  cargarAreas();

  // 🔹 Evento para agregar nueva área
  formArea.addEventListener("submit", async (e) => {
    e.preventDefault();
    const nombre = nombreInput.value.trim();

    if (!nombre) return;

    const resp = await fetch("/api/areas", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ nombre }),
    });

    if (resp.ok) {
      nombreInput.value = "";
      cargarAreas();
    } else {
      alert("⚠️ Error al agregar el área (quizá ya existe).");
    }
  });

  // 🔹 Función para cargar áreas
  async function cargarAreas() {
    listaAreas.innerHTML = "";
    const resp = await fetch("/api/areas");
    const data = await resp.json();

    data.forEach((area) => {
      const col = document.createElement("div");
      col.className = "col-md-4";

      col.innerHTML = `
        <div class="card card-custom">
          <div class="card-body">
            <h5>${area.nombre} <small>(ID: ${area.id})</small></h5>
            <div class="d-flex justify-content-center gap-2 mt-2">
              <button class="btn btn-warning btn-sm" onclick="editarArea(${area.id}, '${area.nombre}')">Editar</button>
              <button class="btn btn-danger btn-sm" onclick="eliminarArea(${area.id})">Eliminar</button>
            </div>
          </div>
        </div>
      `;

      listaAreas.appendChild(col);
    });
  }
});

// 🔹 Editar un área
async function editarArea(id, nombreActual) {
  const nuevoNombre = prompt("✏️ Editar nombre del área:", nombreActual);
  if (nuevoNombre && nuevoNombre.trim() !== "") {
    const resp = await fetch(`/api/areas/${id}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ nombre: nuevoNombre }),
    });
    if (resp.ok) {
      location.reload();
    } else {
      alert("⚠️ Error al actualizar el área.");
    }
  }
}

// 🔹 Eliminar un área
async function eliminarArea(id) {
  if (confirm("🗑️ ¿Seguro que deseas eliminar esta área?")) {
    const resp = await fetch(`/api/areas/${id}`, { method: "DELETE" });
    if (resp.ok) {
      location.reload();
    } else {
      alert("⚠️ No se puede eliminar el área porque tiene datos asociados.");
    }
  }
}
