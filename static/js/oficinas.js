document.addEventListener("DOMContentLoaded", () => {
  const formOficina = document.getElementById("formOficina");
  const listaOficinas = document.getElementById("listaOficinas");
  const selectArea = document.getElementById("idAreaOficina");

  // 🔹 Cargar oficinas al inicio
  cargarOficinas();
  cargarAreas();

  // 🔹 Evento agregar oficina
  formOficina.addEventListener("submit", async (e) => {
    e.preventDefault();

    const oficina = {
      codigo: document.getElementById("codigoOficina").value.trim(),
      idArea: parseInt(selectArea.value),
    };

    const resp = await fetch("/api/oficinas", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(oficina),
    });

    if (resp.ok) {
      formOficina.reset();
      cargarOficinas();
    } else {
      alert("⚠️ Error al agregar oficina (quizá ya existe o el área no es válida).");
    }
  });

  // 🔹 Función cargar oficinas
  async function cargarOficinas() {
    listaOficinas.innerHTML = "";
    const resp = await fetch("/api/oficinas");
    const data = await resp.json();

    data.forEach((oficina) => {
      const col = document.createElement("div");
      col.className = "col-md-6";

      col.innerHTML = `
        <div class="card card-custom">
          <div class="card-body">
            <h5>${oficina.codigo} <small>(ID: ${oficina.id})</small></h5>
            <p>📌 Área: ${oficina.idArea} - ${oficina.areaNombre}</p>
            <div class="d-flex justify-content-center gap-2 mt-2">
              <button class="btn btn-warning btn-sm" onclick="editarOficina(${oficina.id}, '${oficina.codigo}')">Editar</button>
              <button class="btn btn-danger btn-sm" onclick="eliminarOficina(${oficina.id})">Eliminar</button>
            </div>
          </div>
        </div>
      `;

      listaOficinas.appendChild(col);
    });
  }

  // 🔹 Cargar áreas en el select
  async function cargarAreas() {
    const resp = await fetch("/api/areas");
    const data = await resp.json();

    selectArea.innerHTML = "";
    data.forEach((a) => {
      const opt = document.createElement("option");
      opt.value = a.id;
      opt.textContent = `Área ${a.id}: ${a.nombre}`;
      selectArea.appendChild(opt);
    });
  }
});

// 🔹 Editar oficina
async function editarOficina(id, codigoActual) {
  const nuevoCodigo = prompt("✏️ Editar código de la oficina:", codigoActual);
  if (nuevoCodigo && nuevoCodigo.trim() !== "") {
    const resp = await fetch(`/api/oficinas/${id}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ codigo: nuevoCodigo }),
    });
    if (resp.ok) {
      location.reload();
    } else {
      alert("⚠️ Error al actualizar la oficina.");
    }
  }
}

// 🔹 Eliminar oficina
async function eliminarOficina(id) {
  if (confirm("🗑️ ¿Seguro que deseas eliminar esta oficina?")) {
    const resp = await fetch(`/api/oficinas/${id}`, { method: "DELETE" });
    if (resp.ok) {
      location.reload();
    } else {
      alert("⚠️ No se puede eliminar la oficina porque tiene empleados asociados.");
    }
  }
}
