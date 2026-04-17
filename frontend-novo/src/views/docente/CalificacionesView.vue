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
        <router-link to="/docente/dashboard"      class="nav-item">
          <svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="1.8" viewBox="0 0 24 24"><rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/></svg>
          Dashboard
        </router-link>
        <router-link to="/docente/estudiantes"    class="nav-item">
          <svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="1.8" viewBox="0 0 24 24"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>
          Mis Estudiantes
        </router-link>
        <router-link to="/docente/calificaciones" class="nav-item">
          <svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="1.8" viewBox="0 0 24 24"><path d="M12 20h9"/><path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"/></svg>
          Calificaciones
        </router-link>
        <router-link to="/docente/comunicados"    class="nav-item">
          <svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="1.8" viewBox="0 0 24 24"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>
          Comunicados
        </router-link>
      </nav>
      <div class="sidebar-footer">
        <div class="user-info">
          <div class="user-avatar">HM</div>
          <div><strong>Lic. H. Mamani</strong><span>Docente</span></div>
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
          <h1>Calificaciones</h1>
          <p>Registra y edita las notas de tus estudiantes por curso</p>
        </div>
        <button class="btn-exportar">📄 Exportar notas</button>
      </div>

      <!-- Selector de curso -->
      <div class="curso-tabs">
        <button
          v-for="c in cursos" :key="c.id"
          class="curso-tab"
          :class="{ active: cursoActivo === c.id }"
          @click="cursoActivo = c.id"
        >
          <div class="tab-dot" :style="{ background: c.color }"></div>
          {{ c.nombre }}
        </button>
      </div>

      <!-- Stats del curso -->
      <div class="stats-row">
        <div class="stat-card">
          <span class="stat-num" style="color:#00d4ff">{{ promedioCurso }}</span>
          <span class="stat-label">Promedio del grupo</span>
        </div>
        <div class="stat-card">
          <span class="stat-num" style="color:#22c55e">{{ aprobados }}</span>
          <span class="stat-label">Aprobados</span>
        </div>
        <div class="stat-card">
          <span class="stat-num" style="color:#ef4444">{{ reprobados }}</span>
          <span class="stat-label">Reprobados</span>
        </div>
        <div class="stat-card">
          <span class="stat-num" style="color:#ffd700">{{ notaMax }}</span>
          <span class="stat-label">Nota más alta</span>
        </div>
      </div>

      <!-- Tabla de calificaciones -->
      <div class="panel">
        <div class="panel-header">
          <h2>Registro de notas — {{ cursoNombre }}</h2>
          <button class="btn-guardar" @click="guardarNotas">✓ Guardar cambios</button>
        </div>
        <table class="tabla">
          <thead>
            <tr>
              <th>Estudiante</th>
              <th class="th-center">Parcial 1</th>
              <th class="th-center">Parcial 2</th>
              <th class="th-center">Trabajo Final</th>
              <th class="th-center">Participación</th>
              <th class="th-center">Nota Final</th>
              <th class="th-center">Estado</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="est in estudiantesActivos" :key="est.id">
              <td>
                <div class="est-cell">
                  <div class="est-avatar">{{ iniciales(est.nombre) }}</div>
                  <strong>{{ est.nombre }}</strong>
                </div>
              </td>
              <td class="th-center">
                <input
                  class="nota-input"
                  type="number" min="0" max="100"
                  v-model.number="est.p1"
                  @input="recalcular(est)"
                />
              </td>
              <td class="th-center">
                <input
                  class="nota-input"
                  type="number" min="0" max="100"
                  v-model.number="est.p2"
                  @input="recalcular(est)"
                />
              </td>
              <td class="th-center">
                <input
                  class="nota-input"
                  type="number" min="0" max="100"
                  v-model.number="est.tf"
                  @input="recalcular(est)"
                />
              </td>
              <td class="th-center">
                <input
                  class="nota-input"
                  type="number" min="0" max="100"
                  v-model.number="est.part"
                  @input="recalcular(est)"
                />
              </td>
              <td class="th-center">
                <span class="nota-final" :class="notaClase(est.final)">
                  {{ est.final }}
                </span>
              </td>
              <td class="th-center">
                <span class="badge-estado" :class="est.final >= 51 ? 'aprobado' : 'reprobado'">
                  {{ est.final >= 51 ? 'Aprobado' : 'Reprobado' }}
                </span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Alerta guardado -->
      <div class="alert-success" v-if="guardado">
        ✅ Calificaciones guardadas correctamente.
      </div>

    </main>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const cursoActivo = ref(1)
const guardado    = ref(false)

const cursos = ref([
  { id: 1, nombre: 'Python Data Science',   color: '#00d4ff' },
  { id: 2, nombre: 'Machine Learning',       color: '#a855f7' },
  { id: 3, nombre: 'Intro a la IA',          color: '#ffd700' },
])

const cursoNombre = computed(() =>
  cursos.value.find(c => c.id === cursoActivo.value)?.nombre
)

const estudiantes = ref([
  { id: 1, nombre: 'Carolina Chávez', p1: 88, p2: 85, tf: 90, part: 92, final: 89, cursoId: 1 },
  { id: 2, nombre: 'Juan Pérez',       p1: 45, p2: 50, tf: 48, part: 55, final: 48, cursoId: 1 },
  { id: 3, nombre: 'María López',      p1: 65, p2: 70, tf: 68, part: 72, final: 69, cursoId: 1 },
  { id: 4, nombre: 'Carlos Quispe',    p1: 82, p2: 79, tf: 85, part: 88, final: 83, cursoId: 1 },
  { id: 5, nombre: 'Ana Flores',       p1: 76, p2: 80, tf: 74, part: 78, final: 77, cursoId: 1 },
  { id: 6, nombre: 'Luis Condori',     p1: 40, p2: 44, tf: 38, part: 50, final: 42, cursoId: 1 },
  { id: 7, nombre: 'Sofia Mamani',     p1: 91, p2: 88, tf: 94, part: 95, final: 92, cursoId: 2 },
  { id: 8, nombre: 'Diego Torrez',     p1: 73, p2: 75, tf: 70, part: 74, final: 73, cursoId: 2 },
  { id: 9, nombre: 'Valeria Rojas',    p1: 61, p2: 65, tf: 60, part: 68, final: 63, cursoId: 2 },
  { id: 10, nombre: 'Roberto Alvarez', p1: 77, p2: 80, tf: 75, part: 82, final: 78, cursoId: 3 },
])

const estudiantesActivos = computed(() =>
  estudiantes.value.filter(e => e.cursoId === cursoActivo.value)
)

const promedioCurso = computed(() => {
  const arr = estudiantesActivos.value
  if (!arr.length) return 0
  return Math.round(arr.reduce((s, e) => s + e.final, 0) / arr.length)
})

const aprobados  = computed(() => estudiantesActivos.value.filter(e => e.final >= 51).length)
const reprobados = computed(() => estudiantesActivos.value.filter(e => e.final < 51).length)
const notaMax    = computed(() => Math.max(...estudiantesActivos.value.map(e => e.final)))

function iniciales(nombre) {
  return nombre.split(' ').map(n => n[0]).join('').slice(0, 2).toUpperCase()
}

function recalcular(est) {
  est.final = Math.round((est.p1 * 0.25) + (est.p2 * 0.25) + (est.tf * 0.35) + (est.part * 0.15))
}

function notaClase(nota) {
  if (nota >= 75) return 'nota-alta'
  if (nota >= 51) return 'nota-media'
  return 'nota-baja'
}

function guardarNotas() {
  guardado.value = true
  setTimeout(() => guardado.value = false, 3000)
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
.user-avatar { width: 36px; height: 36px; border-radius: 50%; background: linear-gradient(135deg, #0077b6, #ffd700); display: flex; align-items: center; justify-content: center; font-size: 12px; font-weight: 700; flex-shrink: 0; }
.user-info strong { display: block; font-size: 13px; }
.user-info span { font-size: 11px; color: #7a96b0; }
.btn-logout { width: 100%; display: flex; align-items: center; gap: 8px; padding: 9px 14px; background: transparent; border: 1px solid rgba(255,255,255,0.07); border-radius: 8px; color: #7a96b0; font-family: 'Sora', sans-serif; font-size: 13px; cursor: pointer; transition: all 0.2s; }
.btn-logout:hover { border-color: rgba(239,68,68,0.4); color: #fca5a5; }

.main { flex: 1; padding: 36px 40px; overflow-y: auto; }
.top-bar { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 24px; }
.top-bar h1 { font-size: 26px; font-weight: 700; margin-bottom: 4px; }
.top-bar p { font-size: 14px; color: #7a96b0; }
.btn-exportar { padding: 10px 20px; background: rgba(255,215,0,0.1); border: 1px solid rgba(255,215,0,0.25); border-radius: 10px; color: #ffd700; font-family: 'Sora', sans-serif; font-size: 13px; font-weight: 600; cursor: pointer; }
.btn-exportar:hover { background: rgba(255,215,0,0.18); }

.curso-tabs { display: flex; gap: 10px; margin-bottom: 20px; flex-wrap: wrap; }
.curso-tab { display: flex; align-items: center; gap: 8px; padding: 10px 18px; background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.07); border-radius: 100px; color: #7a96b0; font-family: 'Sora', sans-serif; font-size: 13px; cursor: pointer; transition: all 0.2s; }
.curso-tab:hover { border-color: rgba(0,212,255,0.2); color: #f0f8ff; }
.curso-tab.active { background: rgba(0,119,182,0.2); border-color: rgba(0,212,255,0.35); color: #00d4ff; }
.tab-dot { width: 8px; height: 8px; border-radius: 50%; flex-shrink: 0; }

.stats-row { display: grid; grid-template-columns: repeat(4,1fr); gap: 16px; margin-bottom: 20px; }
.stat-card { background: #0a1628; border: 1px solid rgba(0,212,255,0.08); border-radius: 14px; padding: 18px; text-align: center; }
.stat-num { display: block; font-size: 28px; font-weight: 800; margin-bottom: 4px; }
.stat-label { font-size: 11px; color: #7a96b0; text-transform: uppercase; letter-spacing: 0.5px; }

.panel { background: #0a1628; border: 1px solid rgba(0,212,255,0.08); border-radius: 16px; overflow: hidden; margin-bottom: 16px; }
.panel-header { display: flex; justify-content: space-between; align-items: center; padding: 18px 20px; border-bottom: 1px solid rgba(0,212,255,0.08); }
.panel-header h2 { font-size: 15px; font-weight: 600; }
.btn-guardar { padding: 9px 20px; background: linear-gradient(135deg, #0077b6, #00b4d8); border: none; border-radius: 10px; color: white; font-family: 'Sora', sans-serif; font-size: 13px; font-weight: 600; cursor: pointer; }
.btn-guardar:hover { box-shadow: 0 6px 20px rgba(0,180,216,0.35); }

.tabla { width: 100%; border-collapse: collapse; }
.tabla th { padding: 12px 16px; text-align: left; font-size: 11px; font-weight: 600; color: #7a96b0; text-transform: uppercase; letter-spacing: 0.8px; border-bottom: 1px solid rgba(0,212,255,0.08); }
.th-center { text-align: center !important; }
.tabla tbody tr { border-bottom: 1px solid rgba(255,255,255,0.04); transition: background 0.15s; }
.tabla tbody tr:last-child { border-bottom: none; }
.tabla tbody tr:hover { background: rgba(0,212,255,0.03); }
.tabla td { padding: 12px 16px; font-size: 13px; vertical-align: middle; }

.est-cell { display: flex; align-items: center; gap: 10px; }
.est-avatar { width: 32px; height: 32px; border-radius: 50%; background: linear-gradient(135deg, #0077b6, #a855f7); display: flex; align-items: center; justify-content: center; font-size: 11px; font-weight: 700; flex-shrink: 0; }

.nota-input { width: 60px; padding: 7px; background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); border-radius: 8px; color: #f0f8ff; font-family: 'Sora', sans-serif; font-size: 13px; font-weight: 600; text-align: center; outline: none; transition: all 0.2s; }
.nota-input:focus { border-color: rgba(0,212,255,0.5); background: rgba(0,119,182,0.1); }

.nota-final { font-size: 17px; font-weight: 800; }
.nota-alta  { color: #22c55e; }
.nota-media { color: #fbbf24; }
.nota-baja  { color: #ef4444; }

.badge-estado { font-size: 11px; font-weight: 600; padding: 4px 10px; border-radius: 100px; }
.aprobado  { background: rgba(34,197,94,0.12);  color: #22c55e; }
.reprobado { background: rgba(239,68,68,0.12);  color: #ef4444; }

.alert-success { margin-top: 16px; background: rgba(34,197,94,0.1); border: 1px solid rgba(34,197,94,0.25); color: #86efac; border-radius: 12px; padding: 14px 18px; font-size: 13px; font-weight: 500; }
</style>