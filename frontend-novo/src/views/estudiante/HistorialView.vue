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
        <router-link to="/estudiante/dashboard" class="nav-item">
          <svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="1.8" viewBox="0 0 24 24"><rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/></svg>
          Dashboard
        </router-link>
        <router-link to="/estudiante/cursos" class="nav-item">
          <svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="1.8" viewBox="0 0 24 24"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/></svg>
          Catálogo de Cursos
        </router-link>
        <router-link to="/estudiante/perfil" class="nav-item">
          <svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="1.8" viewBox="0 0 24 24"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
          Mi Perfil
        </router-link>
        <router-link to="/estudiante/historial" class="nav-item">
          <svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="1.8" viewBox="0 0 24 24"><path d="M12 20h9"/><path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"/></svg>
          Historial y Notas
        </router-link>
      </nav>
      <div class="sidebar-footer">
        <div class="user-info">
          <div class="user-avatar">CA</div>
          <div><strong>Carolina Ch.</strong><span>Estudiante</span></div>
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
          <h1>Historial y Notas</h1>
          <p>Registro completo de tu trayectoria académica en el LASIN</p>
        </div>
        <button class="btn-exportar">
          📄 Exportar historial
        </button>
      </div>

      <!-- Resumen general -->
      <div class="resumen-grid">
        <div class="resumen-card" v-for="r in resumen" :key="r.label">
          <span class="resumen-icono">{{ r.icono }}</span>
          <span class="resumen-num" :style="{ color: r.color }">{{ r.valor }}</span>
          <span class="resumen-label">{{ r.label }}</span>
        </div>
      </div>

      <!-- Tabs -->
      <div class="tabs">
        <button
          v-for="tab in tabs" :key="tab.value"
          class="tab"
          :class="{ active: tabActivo === tab.value }"
          @click="tabActivo = tab.value"
        >
          {{ tab.label }}
        </button>
      </div>

      <!-- Tabla de cursos completados -->
      <div class="panel" v-if="tabActivo === 'completados'">
        <table class="tabla">
          <thead>
            <tr>
              <th>Curso</th>
              <th>Docente</th>
              <th>Período</th>
              <th>Asistencia</th>
              <th>Nota final</th>
              <th>Estado</th>
              <th>Acciones</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="curso in cursosCompletados" :key="curso.id">
              <td>
                <div class="curso-cell">
                  <div class="curso-dot" :style="{ background: curso.color }"></div>
                  <div>
                    <strong>{{ curso.nombre }}</strong>
                    <span>{{ curso.categoria }}</span>
                  </div>
                </div>
              </td>
              <td class="text-gris">{{ curso.docente }}</td>
              <td class="text-gris">{{ curso.periodo }}</td>
              <td>
                <span class="asistencia" :class="asistenciaClase(curso.asistencia)">
                  {{ curso.asistencia }}%
                </span>
              </td>
              <td>
                <span class="nota" :class="notaClase(curso.nota)">{{ curso.nota }}</span>
              </td>
              <td>
                <span class="badge-estado aprobado" v-if="curso.nota >= 51">Aprobado</span>
                <span class="badge-estado reprobado" v-else>Reprobado</span>
              </td>
              <td>
                <button class="btn-cert" @click="verCertificado(curso)" title="Ver certificado">
                  🏆
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Cursos en curso -->
      <div class="panel" v-if="tabActivo === 'activos'">
        <div class="activo-item" v-for="curso in cursosActivos" :key="curso.id">
          <div class="activo-color" :style="{ background: curso.color }"></div>
          <div class="activo-info">
            <strong>{{ curso.nombre }}</strong>
            <span>{{ curso.docente }} · {{ curso.periodo }}</span>
          </div>
          <div class="activo-progress">
            <div class="prog-label">
              <span>Progreso</span>
              <span class="prog-pct">{{ curso.progreso }}%</span>
            </div>
            <div class="prog-bar">
              <div class="prog-fill" :style="{ width: curso.progreso + '%', background: curso.color }"></div>
            </div>
          </div>
          <div class="activo-nota">
            <span class="nota-parcial">{{ curso.notaParcial }}</span>
            <span class="nota-label">Nota parcial</span>
          </div>
        </div>
      </div>

      <!-- Encuestas pendientes -->
      <div class="panel" v-if="tabActivo === 'encuestas'">
        <div class="encuesta-item" v-for="e in encuestasPendientes" :key="e.id">
          <div class="enc-icon">⭐</div>
          <div class="enc-info">
            <strong>{{ e.curso }}</strong>
            <span>Completado el {{ e.fecha }} · Docente: {{ e.docente }}</span>
          </div>
          <button class="btn-encuesta" @click="responderEncuesta(e)">
            Responder encuesta
          </button>
        </div>
        <div class="sin-encuestas" v-if="encuestasPendientes.length === 0">
          <span>✅</span>
          <p>No tienes encuestas pendientes. ¡Gracias por tu participación!</p>
        </div>
      </div>

    </main>

    <!-- Modal certificado -->
    <div class="modal-overlay" v-if="modalCert" @click="modalCert = false">
      <div class="modal" @click.stop>
        <div class="cert-header">
          <div class="cert-logo">LASIN · UMSA</div>
          <h2>Certificado de Aprobación</h2>
        </div>
        <div class="cert-body">
          <p>Se certifica que</p>
          <h3>Carolina Chávez</h3>
          <p>aprobó satisfactoriamente el curso de</p>
          <h3 class="cert-curso">{{ cursoCert?.nombre }}</h3>
          <div class="cert-meta">
            <div><span>Nota final</span><strong>{{ cursoCert?.nota }}/100</strong></div>
            <div><span>Asistencia</span><strong>{{ cursoCert?.asistencia }}%</strong></div>
            <div><span>Período</span><strong>{{ cursoCert?.periodo }}</strong></div>
          </div>
        </div>
        <div class="cert-footer">
          <button class="btn-cerrar" @click="modalCert = false">Cerrar</button>
          <button class="btn-descargar">⬇ Descargar PDF</button>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref } from 'vue'

const tabActivo = ref('completados')
const modalCert = ref(false)
const cursoCert = ref(null)

const tabs = [
  { value: 'completados', label: '✅ Cursos completados' },
  { value: 'activos',     label: '📚 En curso' },
  { value: 'encuestas',   label: '⭐ Encuestas pendientes' },
]

const resumen = [
  { icono: '🎓', valor: '5',   label: 'Cursos aprobados',  color: '#00d4ff' },
  { icono: '📊', valor: '87',  label: 'Promedio general',  color: '#ffd700' },
  { icono: '📅', valor: '92%', label: 'Asistencia media',  color: '#22c55e' },
  { icono: '🏆', valor: '3',   label: 'Certificados',      color: '#a855f7' },
]

const cursosCompletados = ref([
  { id: 1, nombre: 'HTML, CSS & JavaScript', categoria: 'Desarrollo Web', docente: 'Lic. Quispe',  periodo: 'Sep–Nov 2024', asistencia: 95, nota: 88, color: '#0077b6' },
  { id: 2, nombre: 'Python Básico',           categoria: 'Data Science',   docente: 'Lic. Mamani', periodo: 'Jul–Sep 2024', asistencia: 90, nota: 92, color: '#00d4ff' },
  { id: 3, nombre: 'Excel Avanzado',          categoria: 'Ofimática',      docente: 'Lic. Flores',  periodo: 'May–Jun 2024', asistencia: 88, nota: 76, color: '#22c55e' },
  { id: 4, nombre: 'Fundamentos de Redes',    categoria: 'Redes',          docente: 'Lic. Torrez',  periodo: 'Mar–May 2024', asistencia: 80, nota: 68, color: '#ffd700' },
  { id: 5, nombre: 'Introducción a la IA',    categoria: 'IA',             docente: 'Lic. Mamani', periodo: 'Ene–Feb 2024', asistencia: 98, nota: 95, color: '#a855f7' },
])

const cursosActivos = ref([
  { id: 1, nombre: 'Python para Data Science', docente: 'Lic. Mamani', periodo: 'Ene–Mar 2025', progreso: 65, notaParcial: 84, color: 'linear-gradient(90deg,#0077b6,#00d4ff)' },
  { id: 2, nombre: 'React & Angular Avanzado', docente: 'Lic. Quispe',  periodo: 'Feb–May 2025', progreso: 40, notaParcial: 78, color: 'linear-gradient(90deg,#7c3aed,#a855f7)' },
])

const encuestasPendientes = ref([
  { id: 1, curso: 'HTML, CSS & JavaScript', docente: 'Lic. Quispe', fecha: '30/11/2024' },
])

function notaClase(nota) {
  if (nota >= 80) return 'nota-alta'
  if (nota >= 60) return 'nota-media'
  return 'nota-baja'
}

function asistenciaClase(ast) {
  if (ast >= 85) return 'ast-alta'
  if (ast >= 70) return 'ast-media'
  return 'ast-baja'
}

function verCertificado(curso) {
  cursoCert.value = curso
  modalCert.value = true
}

function responderEncuesta(e) {
  alert(`Abriendo encuesta para: ${e.curso}`)
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;500;600;700&display=swap');
* { box-sizing: border-box; margin: 0; padding: 0; }

.dashboard { font-family: 'Sora', sans-serif; display: flex; min-height: 100vh; background: #0d1b2e; color: #f0f8ff; }

/* Sidebar */
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
.user-avatar { width: 36px; height: 36px; border-radius: 50%; background: linear-gradient(135deg, #0077b6, #a855f7); display: flex; align-items: center; justify-content: center; font-size: 12px; font-weight: 700; flex-shrink: 0; }
.user-info strong { display: block; font-size: 13px; }
.user-info span { font-size: 11px; color: #7a96b0; }
.btn-logout { width: 100%; display: flex; align-items: center; gap: 8px; padding: 9px 14px; background: transparent; border: 1px solid rgba(255,255,255,0.07); border-radius: 8px; color: #7a96b0; font-family: 'Sora', sans-serif; font-size: 13px; cursor: pointer; transition: all 0.2s; }
.btn-logout:hover { border-color: rgba(239,68,68,0.4); color: #fca5a5; }

/* Main */
.main { flex: 1; padding: 36px 40px; overflow-y: auto; }
.top-bar { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 28px; }
.top-bar h1 { font-size: 26px; font-weight: 700; margin-bottom: 4px; }
.top-bar p { font-size: 14px; color: #7a96b0; }
.btn-exportar { padding: 10px 20px; background: rgba(255,215,0,0.1); border: 1px solid rgba(255,215,0,0.25); border-radius: 10px; color: #ffd700; font-family: 'Sora', sans-serif; font-size: 13px; font-weight: 600; cursor: pointer; transition: all 0.2s; }
.btn-exportar:hover { background: rgba(255,215,0,0.18); }

/* Resumen */
.resumen-grid { display: grid; grid-template-columns: repeat(4,1fr); gap: 16px; margin-bottom: 28px; }
.resumen-card { background: #0a1628; border: 1px solid rgba(0,212,255,0.08); border-radius: 16px; padding: 20px; display: flex; flex-direction: column; align-items: center; gap: 6px; }
.resumen-icono { font-size: 24px; }
.resumen-num { font-size: 26px; font-weight: 800; }
.resumen-label { font-size: 11px; color: #7a96b0; text-transform: uppercase; letter-spacing: 0.5px; text-align: center; }

/* Tabs */
.tabs { display: flex; gap: 8px; margin-bottom: 20px; }
.tab { padding: 9px 20px; background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.07); border-radius: 100px; color: #7a96b0; font-family: 'Sora', sans-serif; font-size: 13px; cursor: pointer; transition: all 0.2s; }
.tab:hover { color: #f0f8ff; border-color: rgba(0,212,255,0.2); }
.tab.active { background: rgba(0,119,182,0.2); border-color: rgba(0,212,255,0.35); color: #00d4ff; }

/* Panel */
.panel { background: #0a1628; border: 1px solid rgba(0,212,255,0.08); border-radius: 16px; overflow: hidden; }

/* Tabla */
.tabla { width: 100%; border-collapse: collapse; }
.tabla thead tr { border-bottom: 1px solid rgba(0,212,255,0.08); }
.tabla th { padding: 14px 16px; text-align: left; font-size: 11px; font-weight: 600; color: #7a96b0; text-transform: uppercase; letter-spacing: 0.8px; }
.tabla tbody tr { border-bottom: 1px solid rgba(255,255,255,0.04); transition: background 0.15s; }
.tabla tbody tr:last-child { border-bottom: none; }
.tabla tbody tr:hover { background: rgba(0,212,255,0.04); }
.tabla td { padding: 14px 16px; font-size: 13px; vertical-align: middle; }
.text-gris { color: #7a96b0; }

.curso-cell { display: flex; align-items: center; gap: 12px; }
.curso-dot { width: 4px; height: 36px; border-radius: 4px; flex-shrink: 0; }
.curso-cell strong { display: block; font-size: 13px; font-weight: 600; margin-bottom: 2px; }
.curso-cell span { font-size: 11px; color: #7a96b0; }

.nota { font-size: 15px; font-weight: 700; }
.nota-alta  { color: #22c55e; }
.nota-media { color: #fbbf24; }
.nota-baja  { color: #ef4444; }

.asistencia { font-size: 13px; font-weight: 600; }
.ast-alta  { color: #22c55e; }
.ast-media { color: #fbbf24; }
.ast-baja  { color: #ef4444; }

.badge-estado { font-size: 11px; font-weight: 600; padding: 4px 10px; border-radius: 100px; }
.aprobado  { background: rgba(34,197,94,0.12);  color: #22c55e; }
.reprobado { background: rgba(239,68,68,0.12);  color: #ef4444; }

.btn-cert { background: transparent; border: none; font-size: 18px; cursor: pointer; transition: transform 0.2s; }
.btn-cert:hover { transform: scale(1.2); }

/* Cursos activos */
.activo-item { display: flex; align-items: center; gap: 16px; padding: 18px 20px; border-bottom: 1px solid rgba(255,255,255,0.04); }
.activo-item:last-child { border-bottom: none; }
.activo-color { width: 4px; height: 48px; border-radius: 4px; flex-shrink: 0; }
.activo-info { flex: 1; }
.activo-info strong { display: block; font-size: 14px; font-weight: 600; margin-bottom: 4px; }
.activo-info span { font-size: 12px; color: #7a96b0; }
.activo-progress { width: 200px; }
.prog-label { display: flex; justify-content: space-between; font-size: 11px; color: #7a96b0; margin-bottom: 6px; }
.prog-pct { color: #00d4ff; font-weight: 600; }
.prog-bar { height: 5px; background: rgba(255,255,255,0.06); border-radius: 4px; }
.prog-fill { height: 100%; border-radius: 4px; }
.activo-nota { text-align: center; }
.nota-parcial { display: block; font-size: 22px; font-weight: 800; color: #ffd700; }
.nota-label { font-size: 10px; color: #7a96b0; text-transform: uppercase; }

/* Encuestas */
.encuesta-item { display: flex; align-items: center; gap: 16px; padding: 18px 20px; border-bottom: 1px solid rgba(255,255,255,0.04); }
.encuesta-item:last-child { border-bottom: none; }
.enc-icon { font-size: 28px; }
.enc-info { flex: 1; }
.enc-info strong { display: block; font-size: 14px; font-weight: 600; margin-bottom: 4px; }
.enc-info span { font-size: 12px; color: #7a96b0; }
.btn-encuesta { padding: 9px 18px; background: rgba(255,215,0,0.1); border: 1px solid rgba(255,215,0,0.25); border-radius: 10px; color: #ffd700; font-family: 'Sora', sans-serif; font-size: 12px; font-weight: 600; cursor: pointer; transition: all 0.2s; white-space: nowrap; }
.btn-encuesta:hover { background: rgba(255,215,0,0.2); }
.sin-encuestas { text-align: center; padding: 48px; color: #7a96b0; }
.sin-encuestas span { font-size: 40px; display: block; margin-bottom: 12px; }

/* Modal certificado */
.modal-overlay { position: fixed; inset: 0; background: rgba(0,0,0,0.75); backdrop-filter: blur(6px); display: flex; align-items: center; justify-content: center; z-index: 100; }
.modal { background: #0a1628; border: 1px solid rgba(0,212,255,0.15); border-radius: 20px; width: 460px; overflow: hidden; }
.cert-header { background: linear-gradient(135deg, #0077b6, #00d4ff, #ffd700); padding: 28px; text-align: center; }
.cert-logo { font-size: 11px; font-weight: 700; letter-spacing: 3px; text-transform: uppercase; margin-bottom: 8px; opacity: 0.9; }
.cert-header h2 { font-size: 20px; font-weight: 800; }
.cert-body { padding: 28px; text-align: center; }
.cert-body p { font-size: 13px; color: #7a96b0; margin-bottom: 8px; }
.cert-body h3 { font-size: 22px; font-weight: 800; color: #00d4ff; margin-bottom: 8px; }
.cert-curso { color: #ffd700 !important; font-size: 18px !important; }
.cert-meta { display: flex; justify-content: center; gap: 32px; margin-top: 20px; padding-top: 20px; border-top: 1px solid rgba(0,212,255,0.1); }
.cert-meta div { display: flex; flex-direction: column; gap: 4px; }
.cert-meta span { font-size: 11px; color: #7a96b0; text-transform: uppercase; letter-spacing: 0.5px; }
.cert-meta strong { font-size: 18px; font-weight: 700; color: #f0f8ff; }
.cert-footer { display: flex; gap: 12px; padding: 20px 28px; border-top: 1px solid rgba(0,212,255,0.08); }
.btn-cerrar { flex: 1; padding: 11px; background: transparent; border: 1px solid rgba(255,255,255,0.08); border-radius: 10px; color: #7a96b0; font-family: 'Sora', sans-serif; font-size: 13px; cursor: pointer; }
.btn-descargar { flex: 1; padding: 11px; background: linear-gradient(135deg, #0077b6, #00b4d8); border: none; border-radius: 10px; color: white; font-family: 'Sora', sans-serif; font-size: 13px; font-weight: 600; cursor: pointer; }
.btn-descargar:hover { box-shadow: 0 6px 20px rgba(0,180,216,0.35); }
</style>