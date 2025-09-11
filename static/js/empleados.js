document.addEventListener("DOMContentLoaded", () => {
  const formEmpleado = document.getElementById("formEmpleado");
  const listaEmpleados = document.getElementById("listaEmpleados");
  const areaSelect = document.getElementById("idAreaEmpleado");
  const oficinaSelect = document.getElementById("idOficinaEmpleado");

  // 🔹 Cargar datos iniciales
  cargarEmpleados();
  cargarAreasYOficinas();

  // 🔹 Evento agregar empleado
  formEmpleado.addEventListener("submit", async (e) => {
    e.preventDefault();

    const empleado = {
      identificacion: document.getElementById("identificacion").value.trim(),
      nombre: document.getElementById("nombreEmpleado").value.trim(),
      tipo: document.getElementById("tipoEmpleado").value.trim(),
      subtipo: document.getElementById("subtipoEmpleado").value.trim(),
      idArea: parseInt(areaSelect.value),
      idOficina: parseInt(oficinaSelect.value),
    };

    const resp = await fetch("/api/empleados", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(empleado),
    });

    if (resp.ok) {
      formEmpleado.reset();
      cargarEmpleados();
    } else {
      alert("⚠️ Error al agregar empleado.");
    }
  });

  // 🔹 Función cargar empleados
  async function cargarEmpleados() {
    listaEmpleados.innerHTML = "";
    const resp = await fetch("/api/empleados");
    const data = await resp.json();

    data.forEach((empleado) => {
      const col = document.createElement("div");
      col.className = "col-md-6";

      col.innerHTML = `
        <div class="card card-custom">
          <div class="card-body">
            <h5>${empleado.nombre} <small>(ID: ${empleado.id})</small></h5>
            <p>🪪 ${empleado.identificacion} | 👔 ${empleado.tipo} | 📘 ${empleado.subtipo}</p>
            <p>📌 Área: ${empleado.idArea} - ${empleado.areaNombre} <br> 🏢 Oficina: ${empleado.idOficina} - ${empleado.oficinaCodigo}</p>
            <div class="d-flex justify-content-center gap-2 mt-2">
              <button class="btn btn-warning btn-sm" onclick="editarEmpleado(${empleado.id}, '${empleado.nombre}')">Editar</button>
              <button class="btn btn-danger btn-sm" onclick="eliminarEmpleado(${empleado.id})">Eliminar</button>
            </div>
          </div>
        </div>
      `;

      listaEmpleados.appendChild(col);
    });
  }

  // 🔹 Cargar áreas y oficinas en selects
  async function cargarAreasYOficinas() {
    // Áreas
    const respAreas = await fetch("/api/areas");
    const areas = await respAreas.json();
    areaSelect.innerHTML = "";
    areas.forEach((a) => {
      const opt = document.createElement("option");
      opt.value = a.id;
      opt.textContent = `Área ${a.id}: ${a.nombre}`;
      areaSelect.appendChild(opt);
    });

    // Oficinas
    const respOficinas = await fetch("/api/oficinas");
    const oficinas = await respOficinas.json();
    oficinaSelect.innerHTML = "";
    oficinas.forEach((o) => {
      const opt = document.createElement("option");
      opt.value = o.id;
      opt.textContent = `Oficina ${o.id}: ${o.codigo} (Área ${o.idArea})`;
      oficinaSelect.appendChild(opt);
    });
  }
});

// 🔹 Editar empleado
async function editarEmpleado(id, nombreActual) {
  const nuevoNombre = prompt("✏️ Editar nombre del empleado:", nombreActual);
  if (nuevoNombre && nuevoNombre.trim() !== "") {
    const resp = await fetch(`/api/empleados/${id}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ nombre: nuevoNombre }),
    });
    if (resp.ok) {
      location.reload();
    } else {
      alert("⚠️ Error al actualizar el empleado.");
    }
  }
}

// 🔹 Eliminar empleado
async function eliminarEmpleado(id) {
  if (confirm("🗑️ ¿Seguro que deseas eliminar este empleado?")) {
    const resp = await fetch(`/api/empleados/${id}`, { method: "DELETE" });
    if (resp.ok) {
      location.reload();
    } else {
      alert("⚠️ No se puede eliminar el empleado porque tiene dependencias asociadas.");
    }
  }
}
