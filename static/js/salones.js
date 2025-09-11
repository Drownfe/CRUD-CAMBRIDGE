// ------- Utilidades básicas -------
async function apiGet(url) {
  const r = await fetch(url);
  if (!r.ok) throw new Error(`GET ${url} -> ${r.status}`);
  return r.json();
}

async function apiSend(url, method = "POST", data = null) {
  const r = await fetch(url, {
    method,
    headers: { "Content-Type": "application/json" },
    body: data ? JSON.stringify(data) : null,
  });
  if (!r.ok) {
    const msg = await r.text().catch(() => "");
    throw new Error(`${method} ${url} -> ${r.status} ${msg}`);
  }
  return r.json().catch(() => ({}));
}

function fillSelect(selectEl, options, selected = null) {
  selectEl.innerHTML = `<option value="">Seleccione Área...</option>`;
  for (const a of options) {
    const opt = document.createElement("option");
    opt.value = a.id;
    opt.textContent = `Área ${a.id}: ${a.nombre}`;
    if (selected !== null && Number(selected) === Number(a.id)) {
      opt.selected = true;
    }
    selectEl.appendChild(opt);
  }
}

// ------- Estado -------
let AREAS = [];
let AREAS_MAP = new Map(); // id -> nombre
let modalEditar;

// ------- Referencias DOM -------
const formSalon = document.getElementById("formSalon");
const codigoSalon = document.getElementById("codigoSalon");
const idAreaSalon = document.getElementById("idAreaSalon");

const listaSalones = document.getElementById("listaSalones");

const formEditarSalon = document.getElementById("formEditarSalon");
const editIdSalon = document.getElementById("editIdSalon");
const editCodigoSalon = document.getElementById("editCodigoSalon");
const editIdAreaSalon = document.getElementById("editIdAreaSalon");

// ------- Carga inicial -------
document.addEventListener("DOMContentLoaded", async () => {
  modalEditar = new bootstrap.Modal(document.getElementById("modalEditarSalon"));

  try {
    await cargarAreas();
    await cargarSalones();
  } catch (e) {
    console.error(e);
    alert("Error cargando datos iniciales.");
  }
});

// ------- Cargar Áreas -------
async function cargarAreas() {
  AREAS = await apiGet("/api/areas");
  AREAS_MAP.clear();
  for (const a of AREAS) {
    AREAS_MAP.set(Number(a.id), a.nombre);
  }
  // llenar ambos selects
  fillSelect(idAreaSalon, AREAS);
  fillSelect(editIdAreaSalon, AREAS);
}

// ------- Cargar Salones -------
async function cargarSalones() {
  const salones = await apiGet("/api/salones");
  renderSalones(salones);
}

// ------- Render Cards -------
function renderSalones(salones) {
  listaSalones.innerHTML = "";
  if (!salones.length) {
    listaSalones.innerHTML = `<div class="col-12"><div class="alert alert-info">No hay salones registrados.</div></div>`;
    return;
  }

  for (const s of salones) {
    const areaNombre = AREAS_MAP.get(Number(s.idArea)) || `ID ${s.idArea}`;

    const col = document.createElement("div");
    col.className = "col-12 col-md-6";

    col.innerHTML = `
      <div class="card shadow-sm h-100 text-start">
        <div class="card-body">
          <h5 class="card-title mb-1">Código: <strong>${s.codigo}</strong></h5>
          <p class="card-text text-muted mb-3">Área: ${areaNombre} (ID: ${s.idArea})</p>
          <div class="d-flex gap-2">
            <button class="btn btn-sm btn-warning" data-action="editar" data-id="${s.id}" data-codigo="${s.codigo}" data-idarea="${s.idArea}">Editar</button>
            <button class="btn btn-sm btn-danger" data-action="eliminar" data-id="${s.id}">Eliminar</button>
          </div>
        </div>
      </div>
    `;

    listaSalones.appendChild(col);
  }

  // Delegación de eventos para editar/eliminar
  listaSalones.querySelectorAll("button[data-action]").forEach(btn => {
    btn.addEventListener("click", (ev) => {
      const action = ev.currentTarget.dataset.action;
      const id = ev.currentTarget.dataset.id;

      if (action === "editar") {
        const codigo = ev.currentTarget.dataset.codigo;
        const idArea = ev.currentTarget.dataset.idarea;
        abrirModalEditar(id, codigo, idArea);
      }

      if (action === "eliminar") {
        eliminarSalon(id);
      }
    });
  });
}

// ------- Agregar -------
formSalon.addEventListener("submit", async (e) => {
  e.preventDefault();
  const codigo = codigoSalon.value.trim();
  const idArea = idAreaSalon.value;

  if (!codigo || !idArea) {
    alert("Completa el código del salón y selecciona un Área.");
    return;
  }

  try {
    await apiSend("/api/salones", "POST", { codigo, idArea: Number(idArea) });
    formSalon.reset();
    await cargarSalones();
  } catch (err) {
    console.error(err);
    alert("No se pudo agregar el salón.");
  }
});

// ------- Editar -------
function abrirModalEditar(id, codigo, idArea) {
  editIdSalon.value = id;
  editCodigoSalon.value = codigo;
  fillSelect(editIdAreaSalon, AREAS, Number(idArea));
  modalEditar.show();
}

formEditarSalon.addEventListener("submit", async (e) => {
  e.preventDefault();
  const id = editIdSalon.value;
  const codigo = editCodigoSalon.value.trim();
  const idArea = editIdAreaSalon.value;

  if (!codigo || !idArea) {
    alert("Completa el código del salón y selecciona un Área.");
    return;
  }

  try {
    await apiSend(`/api/salones/${id}`, "PUT", { codigo, idArea: Number(idArea) });
    modalEditar.hide();
    await cargarSalones();
  } catch (err) {
    console.error(err);
    alert("No se pudo actualizar el salón.");
  }
});

// ------- Eliminar -------
async function eliminarSalon(id) {
  if (!confirm("¿Seguro que deseas eliminar este salón?")) return;

  try {
    await apiSend(`/api/salones/${id}`, "DELETE");
    await cargarSalones();
  } catch (err) {
    console.error(err);
    alert("No se pudo eliminar el salón.");
  }
}
