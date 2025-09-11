// ------- Utilidades -------
async function apiSend(url, method = "POST", data = null) {
  const r = await fetch(url, {
    method,
    headers: { "Content-Type": "application/json" },
    body: data ? JSON.stringify(data) : null,
  });
  if (!r.ok) {
    const msg = await r.json().catch(() => ({}));
    throw new Error(msg.message || `⚠️ Error ${method} ${url}`);
  }
  return r.json().catch(() => ({}));
}

// ------- Estado -------
let AREAS = [];
let AREAS_MAP = new Map();
let modalEditar;

// ------- Referencias -------
const formSalon = document.getElementById("formSalon");
const codigoSalon = document.getElementById("codigoSalon");
const idAreaSalon = document.getElementById("idAreaSalon");
const listaSalones = document.getElementById("listaSalones");
const formEditarSalon = document.getElementById("formEditarSalon");
const editIdSalon = document.getElementById("editIdSalon");
const editCodigoSalon = document.getElementById("editCodigoSalon");
const editIdAreaSalon = document.getElementById("editIdAreaSalon");

document.addEventListener("DOMContentLoaded", async () => {
  modalEditar = new bootstrap.Modal(document.getElementById("modalEditarSalon"));
  await cargarAreas();
  await cargarSalones();
});

async function cargarAreas() {
  const resp = await fetch("/api/areas");
  AREAS = await resp.json();
  AREAS_MAP.clear();
  AREAS.forEach((a) => AREAS_MAP.set(Number(a.id), a.nombre));

  fillSelect(idAreaSalon, AREAS);
  fillSelect(editIdAreaSalon, AREAS);
}

async function cargarSalones() {
  const resp = await fetch("/api/salones");
  const salones = await resp.json();
  renderSalones(salones);
}

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

  listaSalones.querySelectorAll("button[data-action]").forEach(btn => {
    btn.addEventListener("click", (ev) => {
      const action = ev.currentTarget.dataset.action;
      const id = ev.currentTarget.dataset.id;

      if (action === "editar") {
        abrirModalEditar(id, ev.currentTarget.dataset.codigo, ev.currentTarget.dataset.idarea);
      }
      if (action === "eliminar") {
        eliminarSalon(id);
      }
    });
  });
}

formSalon.addEventListener("submit", async (e) => {
  e.preventDefault();
  const codigo = codigoSalon.value.trim();
  const idArea = idAreaSalon.value;

  if (!codigo || !idArea) {
    alert("⚠️ Completa el código del salón y selecciona un Área.");
    return;
  }

  try {
    await apiSend("/api/salones", "POST", { codigo, idArea: Number(idArea) });
    formSalon.reset();
    await cargarSalones();
  } catch (err) {
    alert(err.message);
  }
});

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
    alert("⚠️ Completa el código del salón y selecciona un Área.");
    return;
  }

  try {
    await apiSend(`/api/salones/${id}`, "PUT", { codigo, idArea: Number(idArea) });
    modalEditar.hide();
    await cargarSalones();
  } catch (err) {
    alert(err.message);
  }
});

async function eliminarSalon(id) {
  if (!confirm("¿Seguro que deseas eliminar este salón?")) return;

  try {
    await apiSend(`/api/salones/${id}`, "DELETE");
    await cargarSalones();
  } catch (err) {
    alert(err.message);
  }
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
