<template>
  <div class="dashboard">

    <!-- Sidebar -->
    <aside class="sidebar">
      <div class="sidebar-logo">
        <div class="logo-box">
          <svg width="20" height="20" fill="none" stroke="currentColor" stroke-width="1.8" viewBox="0 0 24 24"><path d="M12 2L2 7l10 5 10-5-10-5z"/><path d="M2 17l10 5 10-5"/><path d="M2 12l10 5 10-5"/></svg>
        </div>
        <div><strong>LASIN</strong><span>Sistema v2.0</span></div>
      </div>
      <nav class="sidebar-nav">
        <router-link to="/admin/dashboard"    class="nav-item">
          <svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="1.8" viewBox="0 0 24 24"><rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/></svg>
          Dashboard
        </router-link>
        <router-link to="/admin/preinscritos" class="nav-item">
          <svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="1.8" viewBox="0 0 24 24"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>
          Preinscritos
        </router-link>
        <router-link to="/admin/reportes"     class="nav-item">
          <svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="1.8" viewBox="0 0 24 24"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg>
          Reportes
        </router-link>
      </nav>
      <div class="sidebar-footer">
        <div class="user-info">
          <div class="user-avatar">AD</div>
          <div><strong>Administrador</strong><span>LASIN</span></div>
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
          <h1>Gestión de Preinscritos</h1>
          <p>Verifica pagos y confirma inscripciones oficiales</p>
        </div>
      </div>

      <!-- Filtros -->
      <div class="filtros">
        <div class="search-wrap">
          <svg width="15" height="15" fill="none" stroke="currentColor" stroke-width="1.8" viewBox="0 0 24 24"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/></svg>
          <input v-model="busqueda" type="text" placeholder="Buscar estudiante..."/>
        </div>
        <div class="filtro-tabs">
          <button
            v-for="f in filtros" :key="f.value"
            class="filtro-tab"
            :class="{ active: filtroActivo === f.value }"
            @click="filtroActivo = f.value"
          >
            {{ f.label }}
            <span class="filtro-count">{{ contarPorEstado(f.value) }}</span>
          </button>
        </div>
        <div class="curso-select-wrap">
          <select v-model="cursoFiltro" class="select-input">
            <option value="todos">Todos los cursos</option>
            <option v-for="c in cursos" :key="c.id" :value="c.id">{{ c.nombre }}</option>
          </select>
        </div>
      </div>

      <!-- Tabla -->
      <div class="panel">
        <table class="tabla">
          <thead>
            <tr>
              <th>Estudiante</th>
              <th>Curso</th>
              <th>Fecha preinscripción</th>
              <th>Monto</th>
              <th>Días esperando</th>
              <th>Estado</th>
              <th class="th-center">Acción</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="p in preinscritosFiltrados" :key="p.id">
              <td>
                <div class="est-cell">
                  <div class="est-avatar">{{ iniciales(p.estudiante) }}</div>
                  <div>
                    <strong>{{ p.estudiante }}</strong>
                    <span>{{ p.email }}</span>
                  </div>
                </div>
              </td>
              <td>
                <div class="curso-cell">
                  <div class="curso-dot" :style="{ background: p.cursoColor }"></div>
                  {{ p.curso }}
                </div>
              </td>
              <td class="text-gris">{{ p.fecha }}</td>
              <td class="text-monto">Bs. {{ p.monto }}</td>
              <td>
                <span class="dias-badge" :class="diasClase(p.dias)">
                  {{ p.dias }} {{ p.dias === 1 ? 'día' : 'días' }}
                </span>
              </td>
              <td>
                <span class="badge-estado" :class="p.estado">
                  {{ labelEstado(p.estado) }}
                </span>
              </td>
              <td class="th-center">
                <div class="acciones-btns" v-if="p.estado === 'pendiente'">
                  <button class="btn-confirmar" @click="confirmar(p)" title="Confirmar pago">
                    ✓ Confirmar
                  </button>
                  <button class="btn-rechazar" @click="rechazar(p)" title="Rechazar">
                    ✕
                  </button>
                </div>
                <span class="ya-procesado" v-else>—</span>
              </td>
            </tr>
          </tbody>
        </table>

        <div class="sin-resultados" v-if="preinscritosFiltrados.length === 0">
          <span>🔍</span>
          <p>No hay preinscritos con ese criterio.</p>
        </div>
      </div>

    </main>

    <!-- Modal confirmación -->
    <div class="modal-overlay" v-if="modalVisible" @click="modalVisible = false">
      <div class="modal" @click.stop>
        <div class="modal-icon">{{ modalTipo === 'confirmar' ? '✅' : '⚠️' }}</div>
        <h2>{{ modalTipo === 'confirmar' ? 'Confirmar pago' : 'Rechazar preinscripción' }}</h2>
        <p v-if="modalTipo === 'confirmar'">
          ¿Confirmas que <strong>{{ seleccionado?.estudiante }}</strong> realizó el pago de
          <strong>Bs. {{ seleccionado?.monto }}</strong> para el curso
          <strong>{{ seleccionado?.curso }}</strong>?
        </p>
        <p v-else>
          ¿Estás seguro de rechazar la preinscripción de
          <strong>{{ seleccionado?.estudiante }}</strong> en <strong>{{ seleccionado?.curso }}</strong>?
          Esta acción notificará al estudiante.
        </p>
        <div class="modal-aviso" v-if="modalTipo === 'confirmar'">
          📌 Esta acción cambiará el estado del estudiante a <strong>Inscrito oficialmente</strong>
          y quedará registrada en el log de auditoría.
        </div>
        <div class="modal-btns">
          <button class="btn-cancelar" @click="modalVisible = false">Cancelar</button>
          <button
            class="btn-accion"
            :class="modalTipo"
            @click="ejecutarAccion"
          >
            {{ modalTipo === 'confirmar' ? '✓ Sí, confirmar pago' : '✕ Sí, rechazar' }}
          </button>
        </div>
      </div>
    </div>

    <!-- Toast de éxito -->
    <div class="toast" :class="{ visible: toastVisible, error: toastError }">
      {{ toastMsg }}
    </div>

  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const busqueda    = ref('')
const filtroActivo = ref('todos')
const cursoFiltro  = ref('todos')
const modalVisible = ref(false)
const modalTipo    = ref('confirmar')
const seleccionado = ref(null)
const toastVisible = ref(false)
const toastError   = ref(false)
const toastMsg     = ref('')

const filtros = [
  { value: 'todos',     label: 'Todos'     },
  { value: 'pendiente', label: 'Pendientes' },
  { value: 'inscrito',  label: 'Confirmados'},
  { value: 'rechazado', label: 'Rechazados' },
]

const cursos = ref([
  { id: 1, nombre: 'Python Data Science',  color: '#00d4ff' },
  { id: 2, nombre: 'React & Angular',       color: '#a855f7' },
  { id: 3, nombre: 'Azure Fundamentals',    color: '#0077b6' },
  { id: 4, nombre: 'Machine Learning',      color: '#ffd700' },
  { id: 5, nombre: 'Excel & Power BI',      color: '#22c55e' },
])

const preinscritos = ref([
  { id: 1,  estudiante: 'Juan Pérez',      email: 'juan.p@est.umsa.bo',    curso: 'Python Data Science', cursoColor: '#00d4ff', cursoId: 1, fecha: '14/02/2025', monto: 350, dias: 5, estado: 'pendiente' },
  { id: 2,  estudiante: 'Luis Condori',    email: 'luis.c@est.umsa.bo',    curso: 'Azure Fundamentals',  cursoColor: '#0077b6', cursoId: 3, fecha: '15/02/2025', monto: 380, dias: 4, estado: 'pendiente' },
  { id: 3,  estudiante: 'María López',     email: 'maria.l@est.umsa.bo',   curso: 'React & Angular',     cursoColor: '#a855f7', cursoId: 2, fecha: '16/02/2025', monto: 400, dias: 3, estado: 'pendiente' },
  { id: 4,  estudiante: 'Pedro Vargas',    email: 'pedro.v@est.umsa.bo',   curso: 'Machine Learning',    cursoColor: '#ffd700', cursoId: 4, fecha: '17/02/2025', monto: 480, dias: 2, estado: 'pendiente' },
  { id: 5,  estudiante: 'Rosa Huanca',     email: 'rosa.h@est.umsa.bo',    curso: 'Excel & Power BI',    cursoColor: '#22c55e', cursoId: 5, fecha: '18/02/2025', monto: 250, dias: 1, estado: 'pendiente' },
  { id: 6,  estudiante: 'Carolina Chávez', email: 'carolina@est.umsa.bo',  curso: 'Python Data Science', cursoColor: '#00d4ff', cursoId: 1, fecha: '13/02/2025', monto: 350, dias: 6, estado: 'inscrito'  },
  { id: 7,  estudiante: 'Carlos Quispe',   email: 'carlos.q@est.umsa.bo',  curso: 'React & Angular',     cursoColor: '#a855f7', cursoId: 2, fecha: '12/02/2025', monto: 400, dias: 7, estado: 'inscrito'  },
  { id: 8,  estudiante: 'Diego Torrez',    email: 'diego.t@est.umsa.bo',   curso: 'Azure Fundamentals',  cursoColor: '#0077b6', cursoId: 3, fecha: '10/02/2025', monto: 380, dias: 9, estado: 'rechazado' },
])

const preinscritosFiltrados = computed(() =>
  preinscritos.value.filter(p => {
    const matchBusqueda  = p.estudiante.toLowerCase().includes(busqueda.value.toLowerCase())
    const matchEstado    = filtroActivo.value === 'todos' || p.estado === filtroActivo.value
    const matchCurso     = cursoFiltro.value === 'todos'  || p.cursoId === cursoFiltro.value
    return matchBusqueda && matchEstado && matchCurso
  })
)

function contarPorEstado(estado) {
  if (estado === 'todos') return preinscritos.value.length
  return preinscritos.value.filter(p => p.estado === estado).length
}

function iniciales(nombre) {
  return nombre.split(' ').map(n => n[0]).join('').slice(0, 2).toUpperCase()
}

function diasClase(dias) {
  if (dias >= 5) return 'rojo'
  if (dias >= 3) return 'amarillo'
  return 'verde'
}

function labelEstado(estado) {
  return { pendiente: '⏳ Pendiente', inscrito: '✅ Inscrito', rechazado: '✕ Rechazado' }[estado]
}

function confirmar(p) {
  seleccionado.value = p
  modalTipo.value    = 'confirmar'
  modalVisible.value = true
}

function rechazar(p) {
  seleccionado.value = p
  modalTipo.value    = 'rechazar'
  modalVisible.value = true
}

function ejecutarAccion() {
  const p = seleccionado.value
  if (modalTipo.value === 'confirmar') {
    p.estado = 'inscrito'
    mostrarToast(`✅ ${p.estudiante} inscrito oficialmente en ${p.curso}`)
  } else {
    p.estado = 'rechazado'
    mostrarToast(`Preinscripción de ${p.estudiante} rechazada.`, true)
  }
  modalVisible.value = false
}

function mostrarToast(msg, error = false) {
  toastMsg.value     = msg
  toastError.value   = error
  toastVisible.value = true
  setTimeout(() => toastVisible.value = false, 3500)
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;500;600;700&display=swap');
* { box-sizing: border-box; margin: 0; padding: 0; }

.dashboard { font-family: 'Sora', sans-serif; display: flex; min-height: 100vh; background: #0d1b2e; color: #f0f8ff; }

.sidebar { width: 260px; flex-shrink: 0; background: #0a1628; border-right: 1px solid rgba(0,212,255,0.08); display: flex; flex-direction: column; padding: 28px 20px; }
.sidebar-logo { display: flex; align-items: center; gap: 12px; margin-bottom: 40px; padding: 0 8px; }
.logo-box { width: 40px; height: 40px; background: linear-gradient(135deg, #0077b6, #00d4ff); border-radius: 10px; display: flex; align-items: center; justify-content: center; color: white; flex-shrink: 0; }
.sidebar-logo strong { display: block; font-size: 15px; font-weight: 700; }
.sidebar-logo span { font-size: 11px; color: #7a96b0; }
.sidebar-nav { display: flex; flex-direction: column; gap: 4px; flex: 1; }
.nav-item { display: flex; align-items: center; gap: 12px; padding: 11px 14px; border-radius: 10px; color: #7a96b0; text-decoration: none; font-size: 14px; font-weight: 500; transition: all 0.2s; }
.nav-item:hover { background: rgba(0,212,255,0.06); color: #f0f8ff; }
.nav-item.router-link-active { background: rgba(0,119,182,0.2); color: #00d4ff; }
.sidebar-footer { border-top: 1px solid rgba(0,212,255,0.08); padding-top: 20px; }
.user-info { display: flex; align-items: center; gap: 10px; margin-bottom: 12px; }
.user-avatar { width: 36px; height: 36px; border-radius: 50%; background: linear-gradient(135deg, #0077b6, #22c55e); display: flex; align-items: center; justify-content: center; font-size: 12px; font-weight: 700; flex-shrink: 0; }
.user-info strong { display: block; font-size: 13px; }
.user-info span { font-size: 11px; color: #7a96b0; }
.btn-logout { width: 100%; display: flex; align-items: center; gap: 8px; padding: 9px 14px; background: transparent; border: 1px solid rgba(255,255,255,0.07); border-radius: 8px; color: #7a96b0; font-family: 'Sora', sans-serif; font-size: 13px; cursor: pointer; transition: all 0.2s; }
.btn-logout:hover { border-color: rgba(239,68,68,0.4); color: #fca5a5; }

.main { flex: 1; padding: 36px 40px; overflow-y: auto; }
.top-bar { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 24px; }
.top-bar h1 { font-size: 26px; font-weight: 700; margin-bottom: 4px; }
.top-bar p { font-size: 14px; color: #7a96b0; }

/* Filtros */
.filtros { display: flex; gap: 12px; align-items: center; margin-bottom: 20px; flex-wrap: wrap; }
.search-wrap { position: relative; }
.search-wrap svg { position: absolute; left: 13px; top: 50%; transform: translateY(-50%); color: #7a96b0; pointer-events: none; }
.search-wrap input { padding: 10px 16px 10px 38px; background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.08); border-radius: 10px; color: #f0f8ff; font-family: 'Sora', sans-serif; font-size: 13px; outline: none; width: 200px; }
.search-wrap input::placeholder { color: #7a96b0; }
.search-wrap input:focus { border-color: rgba(0,212,255,0.4); }
.filtro-tabs { display: flex; gap: 6px; }
.filtro-tab { display: flex; align-items: center; gap: 6px; padding: 8px 14px; background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.07); border-radius: 100px; color: #7a96b0; font-family: 'Sora', sans-serif; font-size: 12px; cursor: pointer; transition: all 0.2s; }
.filtro-tab:hover { color: #f0f8ff; border-color: rgba(0,212,255,0.2); }
.filtro-tab.active { background: rgba(0,119,182,0.2); border-color: rgba(0,212,255,0.35); color: #00d4ff; }
.filtro-count { background: rgba(255,255,255,0.08); border-radius: 100px; padding: 1px 6px; font-size: 10px; }
.select-input { padding: 9px 14px; background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.08); border-radius: 10px; color: #f0f8ff; font-family: 'Sora', sans-serif; font-size: 13px; outline: none; }
.select-input option { background: #0a1628; }

/* Tabla */
.panel { background: #0a1628; border: 1px solid rgba(0,212,255,0.08); border-radius: 16px; overflow: hidden; }
.tabla { width: 100%; border-collapse: collapse; }
.tabla thead tr { border-bottom: 1px solid rgba(0,212,255,0.08); }
.tabla th { padding: 13px 16px; text-align: left; font-size: 11px; font-weight: 600; color: #7a96b0; text-transform: uppercase; letter-spacing: 0.8px; }
.th-center { text-align: center !important; }
.tabla tbody tr { border-bottom: 1px solid rgba(255,255,255,0.04); transition: background 0.15s; }
.tabla tbody tr:last-child { border-bottom: none; }
.tabla tbody tr:hover { background: rgba(0,212,255,0.03); }
.tabla td { padding: 13px 16px; font-size: 13px; vertical-align: middle; }
.text-gris { color: #7a96b0; font-size: 12px; }
.text-monto { font-weight: 700; color: #22c55e; }

.est-cell { display: flex; align-items: center; gap: 10px; }
.est-avatar { width: 34px; height: 34px; border-radius: 50%; background: linear-gradient(135deg, #0077b6, #a855f7); display: flex; align-items: center; justify-content: center; font-size: 11px; font-weight: 700; flex-shrink: 0; }
.est-cell strong { display: block; font-size: 13px; font-weight: 600; margin-bottom: 2px; }
.est-cell span { font-size: 11px; color: #7a96b0; }

.curso-cell { display: flex; align-items: center; gap: 8px; font-size: 13px; }
.curso-dot { width: 8px; height: 8px; border-radius: 50%; flex-shrink: 0; }

.dias-badge { font-size: 11px; font-weight: 600; padding: 4px 10px; border-radius: 100px; }
.dias-badge.rojo     { background: rgba(239,68,68,0.15);  color: #f87171; }
.dias-badge.amarillo { background: rgba(251,191,36,0.15); color: #fbbf24; }
.dias-badge.verde    { background: rgba(34,197,94,0.15);  color: #22c55e; }

.badge-estado { font-size: 11px; font-weight: 600; padding: 4px 10px; border-radius: 100px; }
.badge-estado.pendiente  { background: rgba(251,191,36,0.12); color: #fbbf24; }
.badge-estado.inscrito   { background: rgba(34,197,94,0.12);  color: #22c55e; }
.badge-estado.rechazado  { background: rgba(239,68,68,0.12);  color: #f87171; }

.acciones-btns { display: flex; gap: 6px; justify-content: center; }
.btn-confirmar { padding: 7px 14px; background: linear-gradient(135deg, #0077b6, #00b4d8); border: none; border-radius: 8px; color: white; font-family: 'Sora', sans-serif; font-size: 12px; font-weight: 600; cursor: pointer; transition: all 0.2s; white-space: nowrap; }
.btn-confirmar:hover { box-shadow: 0 4px 14px rgba(0,180,216,0.35); }
.btn-rechazar { padding: 7px 10px; background: rgba(239,68,68,0.12); border: 1px solid rgba(239,68,68,0.25); border-radius: 8px; color: #f87171; font-family: 'Sora', sans-serif; font-size: 12px; cursor: pointer; transition: all 0.2s; }
.btn-rechazar:hover { background: rgba(239,68,68,0.25); }
.ya-procesado { color: #7a96b0; font-size: 13px; }

.sin-resultados { text-align: center; padding: 48px; color: #7a96b0; }
.sin-resultados span { font-size: 36px; display: block; margin-bottom: 12px; }

/* Modal */
.modal-overlay { position: fixed; inset: 0; background: rgba(0,0,0,0.75); backdrop-filter: blur(6px); display: flex; align-items: center; justify-content: center; z-index: 100; }
.modal { background: #0a1628; border: 1px solid rgba(0,212,255,0.15); border-radius: 20px; padding: 32px; width: 440px; text-align: center; }
.modal-icon { font-size: 40px; margin-bottom: 16px; }
.modal h2 { font-size: 20px; font-weight: 700; margin-bottom: 12px; }
.modal p { font-size: 14px; color: #7a96b0; line-height: 1.7; margin-bottom: 16px; }
.modal p strong { color: #f0f8ff; }
.modal-aviso { background: rgba(0,212,255,0.08); border: 1px solid rgba(0,212,255,0.2); border-radius: 10px; padding: 12px 16px; font-size: 12px; color: #7a96b0; text-align: left; margin-bottom: 24px; line-height: 1.6; }
.modal-aviso strong { color: #00d4ff; }
.modal-btns { display: flex; gap: 12px; }
.btn-cancelar { flex: 1; padding: 12px; background: transparent; border: 1px solid rgba(255,255,255,0.08); border-radius: 10px; color: #7a96b0; font-family: 'Sora', sans-serif; font-size: 13px; cursor: pointer; }
.btn-accion { flex: 2; padding: 12px; border: none; border-radius: 10px; font-family: 'Sora', sans-serif; font-size: 13px; font-weight: 600; cursor: pointer; transition: all 0.2s; }
.btn-accion.confirmar { background: linear-gradient(135deg, #0077b6, #00b4d8); color: white; }
.btn-accion.rechazar  { background: rgba(239,68,68,0.2); color: #f87171; border: 1px solid rgba(239,68,68,0.3); }

/* Toast */
.toast { position: fixed; bottom: 28px; right: 28px; background: #0a1628; border: 1px solid rgba(34,197,94,0.3); color: #86efac; padding: 14px 22px; border-radius: 12px; font-size: 13px; font-weight: 500; transform: translateY(80px); opacity: 0; transition: all 0.3s; z-index: 200; box-shadow: 0 8px 30px rgba(0,0,0,0.4); }
.toast.visible { transform: translateY(0); opacity: 1; }
.toast.error { border-color: rgba(239,68,68,0.3); color: #fca5a5; }
</style>