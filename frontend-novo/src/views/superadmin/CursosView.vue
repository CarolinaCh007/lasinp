<template>
  <div class="dashboard">

    <!-- Sidebar -->
    <aside class="sidebar">
      <div class="sidebar-logo">
        <div class="logo-box">
          <svg width="20" height="20" fill="none" stroke="currentColor" stroke-width="1.8" viewBox="0 0 24 24"><path d="M12 2L2 7l10 5 10-5-10-5z"/><path d="M2 17l10 5 10-5"/><path d="M2 12l10 5 10-5"/></svg>
        </div>
        <div><strong>LASIN</strong><span>Super Admin</span></div>
      </div>
      <nav class="sidebar-nav">
        <router-link to="/superadmin/dashboard" class="nav-item">
          <svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="1.8" viewBox="0 0 24 24"><rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/></svg>
          Dashboard
        </router-link>
        <router-link to="/superadmin/usuarios" class="nav-item">
          <svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="1.8" viewBox="0 0 24 24"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>
          Usuarios
        </router-link>
        <router-link to="/superadmin/cursos" class="nav-item">
          <svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="1.8" viewBox="0 0 24 24"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/></svg>
          Cursos
        </router-link>
        <router-link to="/superadmin/reportes" class="nav-item">
          <svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="1.8" viewBox="0 0 24 24"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/></svg>
          Reportes
        </router-link>
        <router-link to="/superadmin/auditoria" class="nav-item">
          <svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="1.8" viewBox="0 0 24 24"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg>
          Log de Auditoría
        </router-link>
      </nav>
      <div class="sidebar-footer">
        <div class="user-info">
          <div class="user-avatar">SA</div>
          <div><strong>Super Admin</strong><span>Control total</span></div>
        </div>
        <button class="btn-logout" @click="$router.push('/login')">
          <svg width="16" height="16" fill="none" stroke="currentColor" stroke-width="1.8" viewBox="0 0 24 24"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/><polyline points="16 17 21 12 16 7"/><line x1="21" y1="12" x2="9" y2="12"/></svg>
          Salir
        </button>
      </div>
    </aside>

    <!-- Main -->
    <main class="main">

      <div class="top-bar">
        <div>
          <h1>Gestión de Cursos</h1>
          <p>Crea, edita y administra todos los cursos del LASIN</p>
        </div>
        <button class="btn-nuevo" @click="abrirModalNuevo">+ Nuevo curso</button>
      </div>

      <!-- Filtros -->
      <div class="filtros">
        <div class="search-wrap">
          <svg width="15" height="15" fill="none" stroke="currentColor" stroke-width="1.8" viewBox="0 0 24 24"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/></svg>
          <input v-model="busqueda" type="text" placeholder="Buscar curso..."/>
        </div>
        <div class="filtro-tabs">
          <button
            v-for="f in filtros" :key="f.value"
            class="filtro-tab"
            :class="{ active: filtroEstado === f.value }"
            @click="filtroEstado = f.value"
          >{{ f.label }} <span class="filtro-count">{{ contarPorEstado(f.value) }}</span></button>
        </div>
      </div>

      <!-- Grid de cursos -->
      <div class="cursos-grid">
        <div class="curso-card" v-for="c in cursosFiltrados" :key="c.id">
          <div class="curso-header" :style="{ background: c.color }">
            <span class="curso-emoji">{{ c.icono }}</span>
            <div class="curso-header-actions">
              <span class="estado-badge" :class="c.estado">{{ c.estado }}</span>
            </div>
          </div>
          <div class="curso-body">
            <h3>{{ c.nombre }}</h3>
            <p>{{ c.descripcion }}</p>
            <div class="curso-meta">
              <span>👨‍🏫 {{ c.docente }}</span>
              <span>📅 {{ c.fechaInicio }}</span>
            </div>
            <div class="curso-meta">
              <span>⏱️ {{ c.duracion }}</span>
              <span>💰 Bs. {{ c.precio }}</span>
            </div>
            <div class="cupo-wrap">
              <div class="cupo-label">
                <span>Ocupación</span>
                <span class="cupo-num">{{ c.inscritos }}/{{ c.cupoMax }}</span>
              </div>
              <div class="cupo-bar">
                <div
                  class="cupo-fill"
                  :style="{ width: (c.inscritos / c.cupoMax * 100) + '%', background: c.colorHex }"
                ></div>
              </div>
            </div>
            <div class="curso-footer-btns">
              <button class="btn-editar" @click="editarCurso(c)">✏️ Editar</button>
              <button
                class="btn-estado"
                :class="c.estado === 'activo' ? 'pausar' : 'activar'"
                @click="toggleEstado(c)"
              >
                {{ c.estado === 'activo' ? '⏸ Pausar' : '▶ Activar' }}
              </button>
              <button class="btn-eliminar" @click="eliminarCurso(c)">🗑️</button>
            </div>
          </div>
        </div>
      </div>

      <div class="sin-resultados" v-if="cursosFiltrados.length === 0">
        <span>🔍</span>
        <p>No se encontraron cursos con ese criterio.</p>
      </div>

    </main>

    <!-- Modal crear/editar curso -->
    <div class="modal-overlay" v-if="modalVisible" @click.self="modalVisible = false">
      <div class="modal">
        <div class="modal-header">
          <h2>{{ modoEdicion ? '✏️ Editar curso' : '➕ Nuevo curso' }}</h2>
          <button class="btn-cerrar-modal" @click="modalVisible = false">✕</button>
        </div>
        <div class="modal-body">
          <div class="form-grid">
            <div class="field full">
              <label>Nombre del curso</label>
              <input v-model="form.nombre" type="text" class="text-input" placeholder="Ej: Python para Data Science"/>
            </div>
            <div class="field full">
              <label>Descripción</label>
              <textarea v-model="form.descripcion" class="textarea-input" rows="3" placeholder="Descripción breve del curso..."></textarea>
            </div>
            <div class="field">
              <label>Docente</label>
              <select v-model="form.docente" class="select-input">
                <option>Lic. Mamani</option>
                <option>Lic. Quispe</option>
                <option>Lic. Flores</option>
                <option>Lic. Condori</option>
                <option>Lic. Torrez</option>
              </select>
            </div>
            <div class="field">
              <label>Categoría</label>
              <select v-model="form.categoria" class="select-input">
                <option>Desarrollo Web</option>
                <option>Data Science</option>
                <option>Ciberseguridad</option>
                <option>Cloud</option>
                <option>IA</option>
                <option>Ofimática</option>
              </select>
            </div>
            <div class="field">
              <label>Precio (Bs.)</label>
              <input v-model.number="form.precio" type="number" class="text-input" placeholder="350"/>
            </div>
            <div class="field">
              <label>Cupo máximo</label>
              <input v-model.number="form.cupoMax" type="number" class="text-input" placeholder="25"/>
            </div>
            <div class="field">
              <label>Fecha de inicio</label>
              <input v-model="form.fechaInicio" type="date" class="text-input"/>
            </div>
            <div class="field">
              <label>Duración</label>
              <input v-model="form.duracion" type="text" class="text-input" placeholder="Ej: 3 meses"/>
            </div>
            <div class="field">
              <label>Ícono (emoji)</label>
              <input v-model="form.icono" type="text" class="text-input" placeholder="🐍"/>
            </div>
            <div class="field">
              <label>Horario</label>
              <input v-model="form.horario" type="text" class="text-input" placeholder="Lun/Mié 08:00-10:00"/>
            </div>
          </div>
        </div>
        <div class="modal-footer">
          <button class="btn-cancelar" @click="modalVisible = false">Cancelar</button>
          <button class="btn-guardar" @click="guardarCurso">
            {{ modoEdicion ? '✓ Guardar cambios' : '+ Crear curso' }}
          </button>
        </div>
      </div>
    </div>

    <!-- Toast -->
    <div class="toast" :class="{ visible: toastVisible }">{{ toastMsg }}</div>

  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const busqueda     = ref('')
const filtroEstado = ref('todos')
const modalVisible = ref(false)
const modoEdicion  = ref(false)
const toastVisible = ref(false)
const toastMsg     = ref('')
const cursoEditando = ref(null)

const form = ref({
  nombre: '', descripcion: '', docente: 'Lic. Mamani',
  categoria: 'Desarrollo Web', precio: 350, cupoMax: 25,
  fechaInicio: '', duracion: '3 meses', icono: '📚', horario: ''
})

const filtros = [
  { value: 'todos',   label: 'Todos'    },
  { value: 'activo',  label: '✅ Activos' },
  { value: 'pausado', label: '⏸ Pausados'},
  { value: 'lleno',   label: '🔴 Llenos' },
]

const cursos = ref([
  { id: 1, nombre: 'Python para Data Science',  descripcion: 'Aprende Python enfocado en análisis de datos y visualización.', docente: 'Lic. Mamani', categoria: 'Data Science',   icono: '🐍', color: 'linear-gradient(135deg,#0077b6,#00d4ff)', colorHex: '#00d4ff', fechaInicio: '01/03/2025', duracion: '3 meses', precio: 350, cupoMax: 30, inscritos: 28, estado: 'activo',  horario: 'Lun/Mié 08:00' },
  { id: 2, nombre: 'React & Angular Avanzado',   descripcion: 'Domina los frameworks más demandados del mercado web.',         docente: 'Lic. Quispe',  categoria: 'Desarrollo Web', icono: '⚛️', color: 'linear-gradient(135deg,#a855f7,#7c3aed)', colorHex: '#a855f7', fechaInicio: '05/03/2025', duracion: '4 meses', precio: 400, cupoMax: 25, inscritos: 22, estado: 'activo',  horario: 'Mar/Jue 10:00' },
  { id: 3, nombre: 'Ethical Hacking',            descripcion: 'Fundamentos de ciberseguridad ofensiva con labs prácticos.',   docente: 'Lic. Torrez',  categoria: 'Ciberseguridad', icono: '🔐', color: 'linear-gradient(135deg,#ef4444,#b91c1c)', colorHex: '#ef4444', fechaInicio: '10/03/2025', duracion: '3 meses', precio: 450, cupoMax: 20, inscritos: 20, estado: 'lleno',   horario: 'Vie 14:00'     },
  { id: 4, nombre: 'Azure Fundamentals',         descripcion: 'Preparación para la certificación AZ-900 de Microsoft.',       docente: 'Lic. Condori', categoria: 'Cloud',          icono: '☁️', color: 'linear-gradient(135deg,#0ea5e9,#0284c7)', colorHex: '#0ea5e9', fechaInicio: '15/03/2025', duracion: '2 meses', precio: 380, cupoMax: 20, inscritos: 15, estado: 'activo',  horario: 'Sáb 09:00'     },
  { id: 5, nombre: 'Machine Learning Aplicado',  descripcion: 'Algoritmos de ML con scikit-learn y casos reales.',            docente: 'Lic. Mamani', categoria: 'IA',             icono: '🤖', color: 'linear-gradient(135deg,#f59e0b,#d97706)', colorHex: '#ffd700', fechaInicio: '20/03/2025', duracion: '4 meses', precio: 480, cupoMax: 20, inscritos: 18, estado: 'activo',  horario: 'Mar/Jue 14:00' },
  { id: 6, nombre: 'Excel & Power BI Avanzado',  descripcion: 'Dashboards profesionales y análisis empresarial.',             docente: 'Lic. Flores',  categoria: 'Ofimática',      icono: '📊', color: 'linear-gradient(135deg,#22c55e,#16a34a)', colorHex: '#22c55e', fechaInicio: '01/03/2025', duracion: '2 meses', precio: 250, cupoMax: 20, inscritos: 16, estado: 'activo',  horario: 'Lun/Mié 16:00' },
  { id: 7, nombre: 'Docker & Kubernetes',         descripcion: 'Contenedores y orquestación para entornos modernos.',         docente: 'Lic. Quispe',  categoria: 'Desarrollo Web', icono: '🐳', color: 'linear-gradient(135deg,#06b6d4,#0891b2)', colorHex: '#06b6d4', fechaInicio: '12/03/2025', duracion: '3 meses', precio: 420, cupoMax: 20, inscritos:  0, estado: 'pausado', horario: 'Vie 10:00'     },
])

const cursosFiltrados = computed(() =>
  cursos.value.filter(c => {
    const matchBusqueda = c.nombre.toLowerCase().includes(busqueda.value.toLowerCase())
    const matchEstado   = filtroEstado.value === 'todos' || c.estado === filtroEstado.value
    return matchBusqueda && matchEstado
  })
)

function contarPorEstado(estado) {
  if (estado === 'todos') return cursos.value.length
  return cursos.value.filter(c => c.estado === estado).length
}

function abrirModalNuevo() {
  modoEdicion.value = false
  form.value = { nombre: '', descripcion: '', docente: 'Lic. Mamani', categoria: 'Desarrollo Web', precio: 350, cupoMax: 25, fechaInicio: '', duracion: '3 meses', icono: '📚', horario: '' }
  modalVisible.value = true
}

function editarCurso(c) {
  modoEdicion.value  = true
  cursoEditando.value = c
  form.value = {
    nombre: c.nombre, descripcion: c.descripcion, docente: c.docente,
    categoria: c.categoria, precio: c.precio, cupoMax: c.cupoMax,
    fechaInicio: c.fechaInicio, duracion: c.duracion, icono: c.icono, horario: c.horario
  }
  modalVisible.value = true
}

function guardarCurso() {
  if (!form.value.nombre) { mostrarToast('El nombre del curso es obligatorio.'); return }
  if (modoEdicion.value) {
    Object.assign(cursoEditando.value, {
      nombre: form.value.nombre, descripcion: form.value.descripcion,
      docente: form.value.docente, precio: form.value.precio,
      cupoMax: form.value.cupoMax, duracion: form.value.duracion,
      icono: form.value.icono, horario: form.value.horario
    })
    mostrarToast('✅ Curso actualizado correctamente.')
  } else {
    cursos.value.push({
      id: Date.now(), nombre: form.value.nombre, descripcion: form.value.descripcion,
      docente: form.value.docente, categoria: form.value.categoria,
      icono: form.value.icono || '📚',
      color: 'linear-gradient(135deg,#0077b6,#00d4ff)', colorHex: '#00d4ff',
      fechaInicio: form.value.fechaInicio, duracion: form.value.duracion,
      precio: form.value.precio, cupoMax: form.value.cupoMax,
      inscritos: 0, estado: 'activo', horario: form.value.horario
    })
    mostrarToast('✅ Curso creado correctamente.')
  }
  modalVisible.value = false
}

function toggleEstado(c) {
  c.estado = c.estado === 'activo' ? 'pausado' : 'activo'
  mostrarToast(c.estado === 'activo' ? `▶ ${c.nombre} activado.` : `⏸ ${c.nombre} pausado.`)
}

function eliminarCurso(c) {
  if (confirm(`¿Eliminar "${c.nombre}"? Esta acción no se puede deshacer.`)) {
    cursos.value = cursos.value.filter(x => x.id !== c.id)
    mostrarToast('🗑️ Curso eliminado.')
  }
}

function mostrarToast(msg) {
  toastMsg.value = msg
  toastVisible.value = true
  setTimeout(() => toastVisible.value = false, 3000)
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;500;600;700&display=swap');
* { box-sizing: border-box; margin: 0; padding: 0; }
.dashboard { font-family: 'Sora', sans-serif; display: flex; min-height: 100vh; background: #0d1b2e; color: #f0f8ff; }
.sidebar { width: 260px; flex-shrink: 0; background: #0a1628; border-right: 1px solid rgba(0,212,255,0.08); display: flex; flex-direction: column; padding: 28px 20px; }
.sidebar-logo { display: flex; align-items: center; gap: 12px; margin-bottom: 40px; padding: 0 8px; }
.logo-box { width: 40px; height: 40px; background: linear-gradient(135deg,#0077b6,#00d4ff); border-radius: 10px; display: flex; align-items: center; justify-content: center; color: white; flex-shrink: 0; }
.sidebar-logo strong { display: block; font-size: 15px; font-weight: 700; }
.sidebar-logo span { font-size: 11px; color: #7a96b0; }
.sidebar-nav { display: flex; flex-direction: column; gap: 4px; flex: 1; }
.nav-item { display: flex; align-items: center; gap: 12px; padding: 11px 14px; border-radius: 10px; color: #7a96b0; text-decoration: none; font-size: 14px; font-weight: 500; transition: all 0.2s; }
.nav-item:hover { background: rgba(0,212,255,0.06); color: #f0f8ff; }
.nav-item.router-link-active { background: rgba(0,119,182,0.2); color: #00d4ff; }
.sidebar-footer { border-top: 1px solid rgba(0,212,255,0.08); padding-top: 20px; }
.user-info { display: flex; align-items: center; gap: 10px; margin-bottom: 12px; }
.user-avatar { width: 36px; height: 36px; border-radius: 50%; background: linear-gradient(135deg,#a855f7,#0077b6); display: flex; align-items: center; justify-content: center; font-size: 12px; font-weight: 700; flex-shrink: 0; }
.user-info strong { display: block; font-size: 13px; }
.user-info span { font-size: 11px; color: #7a96b0; }
.btn-logout { width: 100%; display: flex; align-items: center; gap: 8px; padding: 9px 14px; background: transparent; border: 1px solid rgba(255,255,255,0.07); border-radius: 8px; color: #7a96b0; font-family: 'Sora', sans-serif; font-size: 13px; cursor: pointer; transition: all 0.2s; }
.btn-logout:hover { border-color: rgba(239,68,68,0.4); color: #fca5a5; }
.main { flex: 1; padding: 36px 40px; overflow-y: auto; }
.top-bar { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 24px; }
.top-bar h1 { font-size: 26px; font-weight: 700; margin-bottom: 4px; }
.top-bar p { font-size: 14px; color: #7a96b0; }
.btn-nuevo { padding: 11px 22px; background: linear-gradient(135deg,#0077b6,#00b4d8); border: none; border-radius: 10px; color: white; font-family: 'Sora', sans-serif; font-size: 14px; font-weight: 600; cursor: pointer; transition: all 0.2s; white-space: nowrap; }
.btn-nuevo:hover { box-shadow: 0 6px 20px rgba(0,180,216,0.4); }
.filtros { display: flex; gap: 12px; align-items: center; margin-bottom: 24px; flex-wrap: wrap; }
.search-wrap { position: relative; }
.search-wrap svg { position: absolute; left: 13px; top: 50%; transform: translateY(-50%); color: #7a96b0; pointer-events: none; }
.search-wrap input { padding: 10px 16px 10px 38px; background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.08); border-radius: 10px; color: #f0f8ff; font-family: 'Sora', sans-serif; font-size: 13px; outline: none; width: 210px; }
.search-wrap input::placeholder { color: #7a96b0; }
.search-wrap input:focus { border-color: rgba(0,212,255,0.4); }
.filtro-tabs { display: flex; gap: 6px; }
.filtro-tab { display: flex; align-items: center; gap: 6px; padding: 8px 14px; background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.07); border-radius: 100px; color: #7a96b0; font-family: 'Sora', sans-serif; font-size: 12px; cursor: pointer; transition: all 0.2s; }
.filtro-tab:hover { color: #f0f8ff; border-color: rgba(0,212,255,0.2); }
.filtro-tab.active { background: rgba(0,119,182,0.2); border-color: rgba(0,212,255,0.35); color: #00d4ff; }
.filtro-count { background: rgba(255,255,255,0.08); border-radius: 100px; padding: 1px 6px; font-size: 10px; }
.cursos-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 20px; }
.curso-card { background: #0a1628; border: 1px solid rgba(0,212,255,0.08); border-radius: 16px; overflow: hidden; transition: all 0.25s; }
.curso-card:hover { transform: translateY(-3px); border-color: rgba(0,212,255,0.2); box-shadow: 0 10px 36px rgba(0,0,0,0.35); }
.curso-header { padding: 20px; display: flex; justify-content: space-between; align-items: flex-start; min-height: 80px; }
.curso-emoji { font-size: 28px; }
.estado-badge { font-size: 10px; font-weight: 600; padding: 4px 10px; border-radius: 100px; text-transform: capitalize; }
.estado-badge.activo  { background: rgba(34,197,94,0.25);  color: #22c55e; }
.estado-badge.pausado { background: rgba(251,191,36,0.25); color: #fbbf24; }
.estado-badge.lleno   { background: rgba(239,68,68,0.25);  color: #f87171; }
.curso-body { padding: 18px; }
.curso-body h3 { font-size: 15px; font-weight: 700; margin-bottom: 6px; }
.curso-body p { font-size: 12px; color: #7a96b0; line-height: 1.6; margin-bottom: 12px; }
.curso-meta { display: flex; gap: 14px; margin-bottom: 5px; }
.curso-meta span { font-size: 11px; color: #7a96b0; }
.cupo-wrap { margin-top: 14px; margin-bottom: 14px; }
.cupo-label { display: flex; justify-content: space-between; font-size: 11px; color: #7a96b0; margin-bottom: 6px; }
.cupo-num { font-weight: 700; color: #00d4ff; }
.cupo-bar { height: 5px; background: rgba(255,255,255,0.06); border-radius: 4px; }
.cupo-fill { height: 100%; border-radius: 4px; transition: width 0.8s ease; }
.curso-footer-btns { display: flex; gap: 8px; }
.btn-editar { flex: 1; padding: 8px; background: rgba(0,212,255,0.08); border: 1px solid rgba(0,212,255,0.2); border-radius: 8px; color: #00d4ff; font-family: 'Sora', sans-serif; font-size: 12px; font-weight: 600; cursor: pointer; transition: all 0.2s; }
.btn-editar:hover { background: rgba(0,212,255,0.15); }
.btn-estado { flex: 1; padding: 8px; border: 1px solid transparent; border-radius: 8px; font-family: 'Sora', sans-serif; font-size: 12px; font-weight: 600; cursor: pointer; transition: all 0.2s; }
.btn-estado.pausar  { background: rgba(251,191,36,0.1); border-color: rgba(251,191,36,0.25); color: #fbbf24; }
.btn-estado.activar { background: rgba(34,197,94,0.1);  border-color: rgba(34,197,94,0.25);  color: #22c55e; }
.btn-eliminar { width: 34px; padding: 8px; background: rgba(239,68,68,0.08); border: 1px solid rgba(239,68,68,0.2); border-radius: 8px; color: #f87171; cursor: pointer; font-size: 13px; transition: all 0.2s; }
.btn-eliminar:hover { background: rgba(239,68,68,0.2); }
.sin-resultados { text-align: center; padding: 60px; color: #7a96b0; }
.sin-resultados span { font-size: 40px; display: block; margin-bottom: 14px; }
.modal-overlay { position: fixed; inset: 0; background: rgba(0,0,0,0.75); backdrop-filter: blur(6px); display: flex; align-items: center; justify-content: center; z-index: 100; }
.modal { background: #0a1628; border: 1px solid rgba(0,212,255,0.15); border-radius: 20px; width: 560px; max-height: 90vh; overflow-y: auto; }
.modal-header { display: flex; justify-content: space-between; align-items: center; padding: 20px 24px; border-bottom: 1px solid rgba(0,212,255,0.08); position: sticky; top: 0; background: #0a1628; z-index: 1; }
.modal-header h2 { font-size: 16px; font-weight: 700; }
.btn-cerrar-modal { background: transparent; border: none; color: #7a96b0; font-size: 16px; cursor: pointer; }
.btn-cerrar-modal:hover { color: #f0f8ff; }
.modal-body { padding: 24px; }
.form-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
.field { display: flex; flex-direction: column; }
.field.full { grid-column: 1 / -1; }
.field label { font-size: 11px; font-weight: 600; color: #7a96b0; text-transform: uppercase; letter-spacing: 0.8px; margin-bottom: 8px; }
.text-input { width: 100%; padding: 11px 14px; background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.08); border-radius: 10px; color: #f0f8ff; font-family: 'Sora', sans-serif; font-size: 13px; outline: none; transition: all 0.2s; }
.text-input:focus { border-color: rgba(0,212,255,0.4); background: rgba(0,119,182,0.08); }
.text-input::placeholder { color: #7a96b0; }
.textarea-input { width: 100%; padding: 11px 14px; background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.08); border-radius: 10px; color: #f0f8ff; font-family: 'Sora', sans-serif; font-size: 13px; outline: none; resize: vertical; line-height: 1.6; }
.textarea-input::placeholder { color: #7a96b0; }
.textarea-input:focus { border-color: rgba(0,212,255,0.4); }
.select-input { width: 100%; padding: 11px 14px; background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.08); border-radius: 10px; color: #f0f8ff; font-family: 'Sora', sans-serif; font-size: 13px; outline: none; }
.select-input option { background: #0a1628; }
.modal-footer { display: flex; gap: 12px; padding: 16px 24px; border-top: 1px solid rgba(0,212,255,0.08); }
.btn-cancelar { flex: 1; padding: 11px; background: transparent; border: 1px solid rgba(255,255,255,0.08); border-radius: 10px; color: #7a96b0; font-family: 'Sora', sans-serif; font-size: 13px; cursor: pointer; }
.btn-guardar { flex: 2; padding: 11px; background: linear-gradient(135deg,#0077b6,#00b4d8); border: none; border-radius: 10px; color: white; font-family: 'Sora', sans-serif; font-size: 13px; font-weight: 600; cursor: pointer; }
.btn-guardar:hover { box-shadow: 0 6px 20px rgba(0,180,216,0.35); }
.toast { position: fixed; bottom: 28px; right: 28px; background: #0a1628; border: 1px solid rgba(0,212,255,0.3); color: #00d4ff; padding: 14px 22px; border-radius: 12px; font-size: 13px; font-weight: 500; transform: translateY(80px); opacity: 0; transition: all 0.3s; z-index: 200; box-shadow: 0 8px 30px rgba(0,0,0,0.4); }
.toast.visible { transform: translateY(0); opacity: 1; }
</style>