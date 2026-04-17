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
          <h1>Log de Auditoría</h1>
          <p>Registro completo de todas las acciones del sistema</p>
        </div>
        <div class="top-actions">
          <button class="btn-exportar">📄 Exportar log</button>
          <button class="btn-limpiar" @click="confirmarLimpiar">🗑️ Limpiar log</button>
        </div>
      </div>

      <!-- Stats rápidas -->
      <div class="stats-grid">
        <div class="stat" v-for="s in stats" :key="s.label">
          <span class="stat-num" :style="{ color: s.color }">{{ s.valor }}</span>
          <span class="stat-label">{{ s.label }}</span>
        </div>
      </div>

      <!-- Filtros -->
      <div class="filtros">
        <div class="search-wrap">
          <svg width="15" height="15" fill="none" stroke="currentColor" stroke-width="1.8" viewBox="0 0 24 24"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/></svg>
          <input v-model="busqueda" type="text" placeholder="Buscar por usuario, acción, módulo..."/>
        </div>
        <div class="filtro-tabs">
          <button
            v-for="f in filtrosTipo" :key="f.value"
            class="filtro-tab"
            :class="{ active: filtroTipo === f.value }"
            @click="filtroTipo = f.value"
          >{{ f.label }}</button>
        </div>
        <div class="filtro-tabs">
          <button
            v-for="f in filtrosModulo" :key="f.value"
            class="filtro-tab modulo"
            :class="{ active: filtroModulo === f.value }"
            @click="filtroModulo = f.value"
          >{{ f.label }}</button>
        </div>
      </div>

      <!-- Log tabla -->
      <div class="panel">
        <div class="panel-header">
          <h2>📋 Registro de eventos <span class="badge-total">{{ logFiltrado.length }} eventos</span></h2>
          <div class="live-indicator">
            <div class="live-dot"></div>
            <span>En vivo</span>
          </div>
        </div>

        <table class="tabla">
          <thead>
            <tr>
              <th>Timestamp</th>
              <th>Usuario</th>
              <th>Módulo</th>
              <th>Acción</th>
              <th>Detalle</th>
              <th class="th-center">Tipo</th>
              <th>IP</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="e in logPaginado" :key="e.id" :class="'fila-' + e.tipo">
              <td class="td-time">
                <span class="time-date">{{ e.fecha }}</span>
                <span class="time-hora">{{ e.hora }}</span>
              </td>
              <td>
                <div class="user-cell">
                  <div class="user-dot" :class="e.rol"></div>
                  <div>
                    <strong>{{ e.usuario }}</strong>
                    <span>{{ labelRol(e.rol) }}</span>
                  </div>
                </div>
              </td>
              <td><span class="modulo-badge" :class="e.modulo">{{ e.modulo }}</span></td>
              <td class="td-accion">{{ e.accion }}</td>
              <td class="td-detalle text-gris">{{ e.detalle }}</td>
              <td class="th-center">
                <span class="tipo-badge" :class="e.tipo">{{ labelTipo(e.tipo) }}</span>
              </td>
              <td class="td-ip text-gris">{{ e.ip }}</td>
            </tr>
          </tbody>
        </table>

        <!-- Paginación -->
        <div class="paginacion">
          <span class="pag-info">Mostrando {{ paginaInicio + 1 }}–{{ Math.min(paginaFin, logFiltrado.length) }} de {{ logFiltrado.length }}</span>
          <div class="pag-btns">
            <button class="pag-btn" :disabled="paginaActual === 0" @click="paginaActual--">‹ Anterior</button>
            <button
              v-for="n in totalPaginas" :key="n"
              class="pag-btn num"
              :class="{ active: paginaActual === n - 1 }"
              @click="paginaActual = n - 1"
            >{{ n }}</button>
            <button class="pag-btn" :disabled="paginaActual >= totalPaginas - 1" @click="paginaActual++">Siguiente ›</button>
          </div>
        </div>
      </div>

    </main>

    <!-- Toast -->
    <div class="toast" :class="{ visible: toastVisible }">{{ toastMsg }}</div>

  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const busqueda     = ref('')
const filtroTipo   = ref('todos')
const filtroModulo = ref('todos')
const paginaActual = ref(0)
const porPagina    = 12
const toastVisible = ref(false)
const toastMsg     = ref('')

const filtrosTipo = [
  { value: 'todos',   label: 'Todos'     },
  { value: 'success', label: '✅ Éxito'  },
  { value: 'info',    label: 'ℹ️ Info'   },
  { value: 'warning', label: '⚠️ Aviso'  },
  { value: 'error',   label: '❌ Error'  },
]

const filtrosModulo = [
  { value: 'todos',    label: 'Todos'      },
  { value: 'auth',     label: '🔑 Auth'    },
  { value: 'usuarios', label: '👥 Usuarios'},
  { value: 'cursos',   label: '📚 Cursos'  },
  { value: 'pagos',    label: '💰 Pagos'   },
  { value: 'sistema',  label: '⚙️ Sistema' },
]

const stats = ref([
  { label: 'Total eventos hoy',   valor: '247', color: '#00d4ff' },
  { label: 'Acciones exitosas',   valor: '231', color: '#22c55e' },
  { label: 'Advertencias',        valor: '12',  color: '#fbbf24' },
  { label: 'Errores',             valor: '4',   color: '#ef4444' },
  { label: 'Usuarios activos',    valor: '18',  color: '#a855f7' },
  { label: 'Último backup',       valor: '2h',  color: '#7a96b0' },
])

const log = ref([
  { id: 1,  fecha: '19/02/2025', hora: '10:42:03', usuario: 'Super Admin',    rol: 'superadmin', modulo: 'usuarios', accion: 'Crear usuario',         detalle: 'Nuevo usuario: ana.flores@est.umsa.bo',       tipo: 'success', ip: '192.168.1.1'  },
  { id: 2,  fecha: '19/02/2025', hora: '10:38:17', usuario: 'Admin LASIN',    rol: 'admin',      modulo: 'pagos',    accion: 'Confirmar pago',          detalle: 'Estudiante: Juan Pérez — Curso: Python DS',   tipo: 'success', ip: '192.168.1.5'  },
  { id: 3,  fecha: '19/02/2025', hora: '10:35:44', usuario: 'Lic. Mamani',    rol: 'docente',    modulo: 'cursos',   accion: 'Subir material',          detalle: 'Sesión 7 — Python DS: numpy_intro.pdf',       tipo: 'info',    ip: '192.168.1.12' },
  { id: 4,  fecha: '19/02/2025', hora: '10:30:11', usuario: 'Carolina C.',    rol: 'estudiante', modulo: 'auth',     accion: 'Inicio de sesión',        detalle: 'Login exitoso desde Chrome/Windows',          tipo: 'success', ip: '192.168.2.34' },
  { id: 5,  fecha: '19/02/2025', hora: '10:28:05', usuario: 'Juan Pérez',     rol: 'estudiante', modulo: 'auth',     accion: 'Intento fallido',         detalle: 'Contraseña incorrecta — 3er intento',         tipo: 'warning', ip: '192.168.2.40' },
  { id: 6,  fecha: '19/02/2025', hora: '10:25:33', usuario: 'Super Admin',    rol: 'superadmin', modulo: 'sistema',  accion: 'Backup manual',           detalle: 'Backup DB completado — 142 MB',               tipo: 'success', ip: '192.168.1.1'  },
  { id: 7,  fecha: '19/02/2025', hora: '10:20:18', usuario: 'Admin LASIN',    rol: 'admin',      modulo: 'cursos',   accion: 'Crear curso',             detalle: 'Nuevo curso: Docker & Kubernetes',            tipo: 'success', ip: '192.168.1.5'  },
  { id: 8,  fecha: '19/02/2025', hora: '10:15:02', usuario: 'Sistema',        rol: 'sistema',    modulo: 'sistema',  accion: 'Error de conexión BD',    detalle: 'Timeout en pool — reconectado en 2s',         tipo: 'error',   ip: 'localhost'    },
  { id: 9,  fecha: '19/02/2025', hora: '10:10:44', usuario: 'María López',    rol: 'estudiante', modulo: 'pagos',    accion: 'Preinscripción',          detalle: 'Curso: Azure Fundamentals — pendiente pago',  tipo: 'info',    ip: '192.168.3.11' },
  { id: 10, fecha: '19/02/2025', hora: '10:05:29', usuario: 'Lic. Quispe',    rol: 'docente',    modulo: 'cursos',   accion: 'Registrar asistencia',    detalle: 'React & Angular — 22 presentes, 0 ausentes',  tipo: 'success', ip: '192.168.1.15' },
  { id: 11, fecha: '19/02/2025', hora: '09:58:14', usuario: 'Super Admin',    rol: 'superadmin', modulo: 'usuarios', accion: 'Desactivar usuario',      detalle: 'Usuario desactivado: maria.l@est.umsa.bo',    tipo: 'warning', ip: '192.168.1.1'  },
  { id: 12, fecha: '19/02/2025', hora: '09:50:07', usuario: 'Carlos Q.',      rol: 'estudiante', modulo: 'auth',     accion: 'Inicio de sesión',        detalle: 'Login exitoso desde Firefox/Linux',           tipo: 'success', ip: '192.168.2.55' },
  { id: 13, fecha: '18/02/2025', hora: '18:42:31', usuario: 'Sistema',        rol: 'sistema',    modulo: 'sistema',  accion: 'Backup automático',       detalle: 'Backup nocturno completado — 138 MB',         tipo: 'success', ip: 'localhost'    },
  { id: 14, fecha: '18/02/2025', hora: '17:30:12', usuario: 'Admin LASIN',    rol: 'admin',      modulo: 'pagos',    accion: 'Rechazar pago',           detalle: 'Comprobante inválido — Estudiante: X. Cruz',  tipo: 'warning', ip: '192.168.1.5'  },
  { id: 15, fecha: '18/02/2025', hora: '16:15:44', usuario: 'Lic. Flores',    rol: 'docente',    modulo: 'cursos',   accion: 'Guardar calificaciones',  detalle: 'Excel & Power BI — Parcial 1 guardado',       tipo: 'success', ip: '192.168.1.18' },
  { id: 16, fecha: '18/02/2025', hora: '15:04:09', usuario: 'Super Admin',    rol: 'superadmin', modulo: 'sistema',  accion: 'Actualizar config.',      detalle: 'JWT expiry cambiado a 24h',                   tipo: 'info',    ip: '192.168.1.1'  },
  { id: 17, fecha: '18/02/2025', hora: '14:22:53', usuario: 'Sistema',        rol: 'sistema',    modulo: 'sistema',  accion: 'Error: memoria alta',     detalle: 'RAM al 89% — alerta generada',                tipo: 'error',   ip: 'localhost'    },
  { id: 18, fecha: '18/02/2025', hora: '13:11:37', usuario: 'Lic. Condori',   rol: 'docente',    modulo: 'cursos',   accion: 'Enviar comunicado',       detalle: 'Azure Fundamentals — Recordatorio examen',    tipo: 'info',    ip: '192.168.1.22' },
  { id: 19, fecha: '18/02/2025', hora: '11:48:20', usuario: 'Super Admin',    rol: 'superadmin', modulo: 'usuarios', accion: 'Resetear contraseña',     detalle: 'Password reset: juan.p@est.umsa.bo',          tipo: 'warning', ip: '192.168.1.1'  },
  { id: 20, fecha: '18/02/2025', hora: '10:33:05', usuario: 'Admin LASIN',    rol: 'admin',      modulo: 'pagos',    accion: 'Confirmar pago',          detalle: 'Estudiante: Carlos Quispe — Machine ML',      tipo: 'success', ip: '192.168.1.5'  },
  { id: 21, fecha: '17/02/2025', hora: '16:55:11', usuario: 'Sistema',        rol: 'sistema',    modulo: 'sistema',  accion: 'Backup automático',       detalle: 'Backup nocturno completado — 135 MB',         tipo: 'success', ip: 'localhost'    },
  { id: 22, fecha: '17/02/2025', hora: '15:40:28', usuario: 'Super Admin',    rol: 'superadmin', modulo: 'cursos',   accion: 'Pausar curso',            detalle: 'Docker & Kubernetes pausado por admin',       tipo: 'warning', ip: '192.168.1.1'  },
  { id: 23, fecha: '17/02/2025', hora: '14:12:44', usuario: 'Lic. Torrez',    rol: 'docente',    modulo: 'cursos',   accion: 'Registrar asistencia',    detalle: 'Ethical Hacking — 20 presentes, 0 ausentes',  tipo: 'success', ip: '192.168.1.20' },
  { id: 24, fecha: '17/02/2025', hora: '11:08:19', usuario: 'Ana Flores',     rol: 'estudiante', modulo: 'auth',     accion: 'Registro nuevo usuario',  detalle: 'Cuenta creada: ana.flores@est.umsa.bo',       tipo: 'success', ip: '192.168.4.7'  },
])

const logFiltrado = computed(() => {
  let l = log.value
  if (filtroTipo.value !== 'todos')   l = l.filter(e => e.tipo === filtroTipo.value)
  if (filtroModulo.value !== 'todos') l = l.filter(e => e.modulo === filtroModulo.value)
  if (busqueda.value)
    l = l.filter(e =>
      e.usuario.toLowerCase().includes(busqueda.value.toLowerCase()) ||
      e.accion.toLowerCase().includes(busqueda.value.toLowerCase())  ||
      e.detalle.toLowerCase().includes(busqueda.value.toLowerCase()) ||
      e.modulo.toLowerCase().includes(busqueda.value.toLowerCase())
    )
  return l
})

const totalPaginas = computed(() => Math.ceil(logFiltrado.value.length / porPagina))
const paginaInicio = computed(() => paginaActual.value * porPagina)
const paginaFin    = computed(() => paginaInicio.value + porPagina)
const logPaginado  = computed(() => logFiltrado.value.slice(paginaInicio.value, paginaFin.value))

function labelRol(rol) {
  return { estudiante: 'Estudiante', docente: 'Docente', admin: 'Admin', superadmin: 'Super Admin', sistema: 'Sistema' }[rol] || rol
}

function labelTipo(tipo) {
  return { success: '✅ Éxito', info: 'ℹ️ Info', warning: '⚠️ Aviso', error: '❌ Error' }[tipo] || tipo
}

function confirmarLimpiar() {
  if (confirm('¿Limpiar todo el log de auditoría? Esta acción no se puede deshacer.')) {
    log.value = []
    mostrarToast('🗑️ Log limpiado correctamente.')
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
.top-bar { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 20px; }
.top-bar h1 { font-size: 26px; font-weight: 700; margin-bottom: 4px; }
.top-bar p { font-size: 14px; color: #7a96b0; }
.top-actions { display: flex; gap: 10px; }
.btn-exportar { padding: 9px 18px; background: rgba(0,212,255,0.08); border: 1px solid rgba(0,212,255,0.2); border-radius: 10px; color: #00d4ff; font-family: 'Sora', sans-serif; font-size: 12px; font-weight: 600; cursor: pointer; transition: all 0.2s; white-space: nowrap; }
.btn-exportar:hover { background: rgba(0,212,255,0.15); }
.btn-limpiar { padding: 9px 18px; background: rgba(239,68,68,0.08); border: 1px solid rgba(239,68,68,0.2); border-radius: 10px; color: #f87171; font-family: 'Sora', sans-serif; font-size: 12px; font-weight: 600; cursor: pointer; transition: all 0.2s; white-space: nowrap; }
.btn-limpiar:hover { background: rgba(239,68,68,0.18); }
.stats-grid { display: grid; grid-template-columns: repeat(6,1fr); gap: 12px; margin-bottom: 20px; }
.stat { background: #0a1628; border: 1px solid rgba(0,212,255,0.08); border-radius: 14px; padding: 16px; text-align: center; }
.stat-num { display: block; font-size: 22px; font-weight: 800; margin-bottom: 4px; }
.stat-label { font-size: 10px; color: #7a96b0; text-transform: uppercase; letter-spacing: 0.5px; }
.filtros { display: flex; gap: 10px; align-items: center; margin-bottom: 18px; flex-wrap: wrap; }
.search-wrap { position: relative; }
.search-wrap svg { position: absolute; left: 13px; top: 50%; transform: translateY(-50%); color: #7a96b0; pointer-events: none; }
.search-wrap input { padding: 10px 16px 10px 38px; background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.08); border-radius: 10px; color: #f0f8ff; font-family: 'Sora', sans-serif; font-size: 13px; outline: none; width: 240px; }
.search-wrap input::placeholder { color: #7a96b0; }
.search-wrap input:focus { border-color: rgba(0,212,255,0.4); }
.filtro-tabs { display: flex; gap: 5px; flex-wrap: wrap; }
.filtro-tab { padding: 7px 13px; background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.07); border-radius: 100px; color: #7a96b0; font-family: 'Sora', sans-serif; font-size: 11px; cursor: pointer; transition: all 0.2s; }
.filtro-tab:hover { color: #f0f8ff; border-color: rgba(0,212,255,0.2); }
.filtro-tab.active { background: rgba(0,119,182,0.2); border-color: rgba(0,212,255,0.35); color: #00d4ff; }
.panel { background: #0a1628; border: 1px solid rgba(0,212,255,0.08); border-radius: 16px; overflow: hidden; }
.panel-header { display: flex; justify-content: space-between; align-items: center; padding: 18px 20px; border-bottom: 1px solid rgba(0,212,255,0.08); }
.panel-header h2 { font-size: 15px; font-weight: 600; display: flex; align-items: center; gap: 10px; }
.badge-total { background: rgba(0,212,255,0.12); color: #00d4ff; font-size: 11px; font-weight: 700; padding: 3px 10px; border-radius: 100px; }
.live-indicator { display: flex; align-items: center; gap: 6px; font-size: 12px; color: #22c55e; }
.live-dot { width: 7px; height: 7px; border-radius: 50%; background: #22c55e; animation: pulse 1.5s infinite; }
@keyframes pulse { 0%,100%{opacity:1;transform:scale(1)} 50%{opacity:0.5;transform:scale(1.3)} }
.tabla { width: 100%; border-collapse: collapse; }
.tabla thead tr { border-bottom: 1px solid rgba(0,212,255,0.08); }
.tabla th { padding: 12px 14px; text-align: left; font-size: 10px; font-weight: 600; color: #7a96b0; text-transform: uppercase; letter-spacing: 0.8px; white-space: nowrap; }
.th-center { text-align: center !important; }
.tabla tbody tr { border-bottom: 1px solid rgba(255,255,255,0.04); transition: background 0.15s; }
.tabla tbody tr:hover { background: rgba(0,212,255,0.03); }
.fila-error   { border-left: 3px solid #ef4444; }
.fila-warning { border-left: 3px solid #fbbf24; }
.fila-success { border-left: 3px solid transparent; }
.fila-info    { border-left: 3px solid transparent; }
.tabla td { padding: 11px 14px; font-size: 12px; vertical-align: middle; }
.td-time { white-space: nowrap; }
.time-date { display: block; font-size: 11px; color: #7a96b0; }
.time-hora { display: block; font-size: 12px; font-weight: 600; color: #00d4ff; font-family: monospace; }
.user-cell { display: flex; align-items: center; gap: 8px; }
.user-dot { width: 8px; height: 8px; border-radius: 50%; flex-shrink: 0; }
.user-dot.superadmin { background: #a855f7; }
.user-dot.admin      { background: #22c55e; }
.user-dot.docente    { background: #ffd700; }
.user-dot.estudiante { background: #00d4ff; }
.user-dot.sistema    { background: #7a96b0; }
.user-cell strong { display: block; font-size: 12px; margin-bottom: 1px; }
.user-cell span { font-size: 10px; color: #7a96b0; }
.modulo-badge { font-size: 10px; font-weight: 600; padding: 3px 9px; border-radius: 100px; text-transform: capitalize; }
.modulo-badge.auth     { background: rgba(168,85,247,0.15); color: #a855f7; }
.modulo-badge.usuarios { background: rgba(0,212,255,0.12);  color: #00d4ff; }
.modulo-badge.cursos   { background: rgba(0,119,182,0.15);  color: #00b4d8; }
.modulo-badge.pagos    { background: rgba(34,197,94,0.12);  color: #22c55e; }
.modulo-badge.sistema  { background: rgba(251,191,36,0.12); color: #fbbf24; }
.td-accion  { font-weight: 600; font-size: 12px; white-space: nowrap; }
.td-detalle { font-size: 11px; max-width: 220px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.text-gris  { color: #7a96b0; }
.tipo-badge { font-size: 10px; font-weight: 600; padding: 4px 10px; border-radius: 100px; white-space: nowrap; }
.tipo-badge.success { background: rgba(34,197,94,0.12);  color: #22c55e; }
.tipo-badge.info    { background: rgba(0,212,255,0.12);  color: #00d4ff; }
.tipo-badge.warning { background: rgba(251,191,36,0.12); color: #fbbf24; }
.tipo-badge.error   { background: rgba(239,68,68,0.12);  color: #f87171; }
.td-ip { font-family: monospace; font-size: 11px; }
.paginacion { display: flex; justify-content: space-between; align-items: center; padding: 16px 20px; border-top: 1px solid rgba(0,212,255,0.08); }
.pag-info { font-size: 12px; color: #7a96b0; }
.pag-btns { display: flex; gap: 6px; align-items: center; }
.pag-btn { padding: 6px 12px; background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.08); border-radius: 8px; color: #7a96b0; font-family: 'Sora', sans-serif; font-size: 12px; cursor: pointer; transition: all 0.2s; }
.pag-btn:hover:not(:disabled) { border-color: rgba(0,212,255,0.3); color: #00d4ff; }
.pag-btn:disabled { opacity: 0.35; cursor: not-allowed; }
.pag-btn.num.active { background: rgba(0,119,182,0.25); border-color: rgba(0,212,255,0.4); color: #00d4ff; font-weight: 700; }
.toast { position: fixed; bottom: 28px; right: 28px; background: #0a1628; border: 1px solid rgba(0,212,255,0.3); color: #00d4ff; padding: 14px 22px; border-radius: 12px; font-size: 13px; font-weight: 500; transform: translateY(80px); opacity: 0; transition: all 0.3s; z-index: 200; box-shadow: 0 8px 30px rgba(0,0,0,0.4); }
.toast.visible { transform: translateY(0); opacity: 1; }
</style>