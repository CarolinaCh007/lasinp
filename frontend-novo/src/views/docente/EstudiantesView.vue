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
          <h1>Mis Estudiantes</h1>
          <p>Lista de inscritos y control de asistencia por curso</p>
        </div>
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
          <span class="tab-count">{{ c.inscritos }}</span>
        </button>
      </div>

      <!-- Barra de acciones -->
      <div class="acciones-bar">
        <div class="search-wrap">
          <svg width="15" height="15" fill="none" stroke="currentColor" stroke-width="1.8" viewBox="0 0 24 24"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/></svg>
          <input v-model="busqueda" type="text" placeholder="Buscar estudiante..."/>
        </div>
        <div class="acciones-right">
          <span class="fecha-label">📅 Clase de hoy: {{ fechaHoy }}</span>
          <button class="btn-guardar-asistencia" @click="guardarAsistencia">
            ✓ Guardar asistencia
          </button>
        </div>
      </div>

      <!-- Tabla de estudiantes -->
      <div class="panel">
        <table class="tabla">
          <thead>
            <tr>
              <th>Estudiante</th>
              <th>Correo</th>
              <th>Asistencia</th>
              <th>Nota parcial</th>
              <th>Estado</th>
              <th class="th-center">Hoy</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="est in estudiantesFiltrados" :key="est.id">
              <td>
                <div class="est-cell">
                  <div class="est-avatar">{{ iniciales(est.nombre) }}</div>
                  <div>
                    <strong>{{ est.nombre }}</strong>
                    <span>{{ est.carrera }}</span>
                  </div>
                </div>
              </td>
              <td class="text-gris">{{ est.email }}</td>
              <td>
                <div class="asist-wrap">
                  <div class="asist-bar">
                    <div
                      class="asist-fill"
                      :style="{ width: est.asistencia + '%' }"
                      :class="asistClase(est.asistencia)"
                    ></div>
                  </div>
                  <span :class="asistClase(est.asistencia)">{{ est.asistencia }}%</span>
                </div>
              </td>
              <td>
                <span class="nota" :class="notaClase(est.notaParcial)">
                  {{ est.notaParcial }}
                </span>
              </td>
              <td>
                <span class="badge-riesgo" :class="est.riesgo">
                  {{ est.riesgo === 'ok' ? '✅ Regular' : est.riesgo === 'medio' ? '⚠️ Atención' : '🔴 Riesgo' }}
                </span>
              </td>
              <td class="th-center">
                <div class="asist-toggle">
                  <button
                    class="toggle-btn"
                    :class="{ presente: est.hoy === 'P', ausente: est.hoy === 'A' }"
                    @click="toggleAsistencia(est, 'P')"
                  >P</button>
                  <button
                    class="toggle-btn"
                    :class="{ presente: est.hoy === 'A', ausente: est.hoy === 'P' }"
                    @click="toggleAsistencia(est, 'A')"
                  >A</button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Resumen asistencia de hoy -->
      <div class="resumen-hoy">
        <div class="res-item res-p">
          <span class="res-num">{{ presentes }}</span>
          <span class="res-label">Presentes</span>
        </div>
        <div class="res-item res-a">
          <span class="res-num">{{ ausentes }}</span>
          <span class="res-label">Ausentes</span>
        </div>
        <div class="res-item res-total">
          <span class="res-num">{{ estudiantesFiltrados.length }}</span>
          <span class="res-label">Total</span>
        </div>
      </div>

      <!-- Alerta guardado -->
      <div class="alert-success" v-if="guardado">
        ✅ Asistencia del {{ fechaHoy }} guardada correctamente.
      </div>

    </main>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const busqueda    = ref('')
const cursoActivo = ref(1)
const guardado    = ref(false)

const fechaHoy = computed(() =>
  new Date().toLocaleDateString('es-BO', { day: '2-digit', month: '2-digit', year: 'numeric' })
)

const cursos = ref([
  { id: 1, nombre: 'Python Data Science',   inscritos: 28, color: '#00d4ff' },
  { id: 2, nombre: 'Machine Learning',       inscritos: 22, color: '#a855f7' },
  { id: 3, nombre: 'Intro a la IA',          inscritos: 17, color: '#ffd700' },
])

const estudiantes = ref([
  { id: 1,  nombre: 'Carolina Chávez',   carrera: 'Informática', email: 'carolina@est.umsa.bo',  asistencia: 95, notaParcial: 88, riesgo: 'ok',    hoy: 'P', cursoId: 1 },
  { id: 2,  nombre: 'Juan Pérez',         carrera: 'Informática', email: 'juan.p@est.umsa.bo',    asistencia: 60, notaParcial: 48, riesgo: 'alto',   hoy: 'A', cursoId: 1 },
  { id: 3,  nombre: 'María López',        carrera: 'Informática', email: 'maria.l@est.umsa.bo',   asistencia: 75, notaParcial: 65, riesgo: 'medio',  hoy: 'P', cursoId: 1 },
  { id: 4,  nombre: 'Carlos Quispe',      carrera: 'Sistemas',    email: 'carlos.q@est.umsa.bo',  asistencia: 90, notaParcial: 82, riesgo: 'ok',     hoy: 'P', cursoId: 1 },
  { id: 5,  nombre: 'Ana Flores',         carrera: 'Informática', email: 'ana.f@est.umsa.bo',     asistencia: 88, notaParcial: 79, riesgo: 'ok',     hoy: 'P', cursoId: 1 },
  { id: 6,  nombre: 'Luis Condori',       carrera: 'Informática', email: 'luis.c@est.umsa.bo',    asistencia: 55, notaParcial: 42, riesgo: 'alto',   hoy: 'A', cursoId: 1 },
  { id: 7,  nombre: 'Sofia Mamani',       carrera: 'Sistemas',    email: 'sofia.m@est.umsa.bo',   asistencia: 92, notaParcial: 91, riesgo: 'ok',     hoy: 'P', cursoId: 2 },
  { id: 8,  nombre: 'Diego Torrez',       carrera: 'Informática', email: 'diego.t@est.umsa.bo',   asistencia: 80, notaParcial: 73, riesgo: 'ok',     hoy: 'P', cursoId: 2 },
  { id: 9,  nombre: 'Valeria Rojas',      carrera: 'Informática', email: 'valeria.r@est.umsa.bo', asistencia: 70, notaParcial: 61, riesgo: 'medio',  hoy: 'P', cursoId: 2 },
  { id: 10, nombre: 'Roberto Alvarez',    carrera: 'Sistemas',    email: 'roberto.a@est.umsa.bo', asistencia: 85, notaParcial: 77, riesgo: 'ok',     hoy: 'A', cursoId: 3 },
])

const estudiantesFiltrados = computed(() =>
  estudiantes.value.filter(e =>
    e.cursoId === cursoActivo.value &&
    e.nombre.toLowerCase().includes(busqueda.value.toLowerCase())
  )
)

const presentes = computed(() => estudiantesFiltrados.value.filter(e => e.hoy === 'P').length)
const ausentes  = computed(() => estudiantesFiltrados.value.filter(e => e.hoy === 'A').length)

function iniciales(nombre) {
  return nombre.split(' ').map(n => n[0]).join('').slice(0, 2).toUpperCase()
}

function toggleAsistencia(est, valor) {
  est.hoy = valor
}

function notaClase(nota) {
  if (nota >= 75) return 'nota-alta'
  if (nota >= 51) return 'nota-media'
  return 'nota-baja'
}

function asistClase(pct) {
  if (pct >= 80) return 'ast-alta'
  if (pct >= 65) return 'ast-media'
  return 'ast-baja'
}

function guardarAsistencia() {
  // Aquí irá la llamada a Flask
  guardado.value = true
  setTimeout(() => guardado.value = false, 3000)
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
.user-avatar { width: 36px; height: 36px; border-radius: 50%; background: linear-gradient(135deg, #0077b6, #ffd700); display: flex; align-items: center; justify-content: center; font-size: 12px; font-weight: 700; flex-shrink: 0; }
.user-info strong { display: block; font-size: 13px; }
.user-info span { font-size: 11px; color: #7a96b0; }
.btn-logout { width: 100%; display: flex; align-items: center; gap: 8px; padding: 9px 14px; background: transparent; border: 1px solid rgba(255,255,255,0.07); border-radius: 8px; color: #7a96b0; font-family: 'Sora', sans-serif; font-size: 13px; cursor: pointer; transition: all 0.2s; }
.btn-logout:hover { border-color: rgba(239,68,68,0.4); color: #fca5a5; }

/* Main */
.main { flex: 1; padding: 36px 40px; overflow-y: auto; }
.top-bar { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 24px; }
.top-bar h1 { font-size: 26px; font-weight: 700; margin-bottom: 4px; }
.top-bar p { font-size: 14px; color: #7a96b0; }

/* Curso tabs */
.curso-tabs { display: flex; gap: 10px; margin-bottom: 20px; flex-wrap: wrap; }
.curso-tab { display: flex; align-items: center; gap: 8px; padding: 10px 18px; background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.07); border-radius: 100px; color: #7a96b0; font-family: 'Sora', sans-serif; font-size: 13px; font-weight: 500; cursor: pointer; transition: all 0.2s; }
.curso-tab:hover { border-color: rgba(0,212,255,0.2); color: #f0f8ff; }
.curso-tab.active { background: rgba(0,119,182,0.2); border-color: rgba(0,212,255,0.35); color: #00d4ff; }
.tab-dot { width: 8px; height: 8px; border-radius: 50%; flex-shrink: 0; }
.tab-count { background: rgba(255,255,255,0.08); border-radius: 100px; padding: 1px 8px; font-size: 11px; }

/* Acciones */
.acciones-bar { display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; gap: 16px; }
.search-wrap { position: relative; }
.search-wrap svg { position: absolute; left: 13px; top: 50%; transform: translateY(-50%); color: #7a96b0; pointer-events: none; }
.search-wrap input { padding: 10px 16px 10px 38px; background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.08); border-radius: 10px; color: #f0f8ff; font-family: 'Sora', sans-serif; font-size: 13px; outline: none; width: 220px; }
.search-wrap input::placeholder { color: #7a96b0; }
.search-wrap input:focus { border-color: rgba(0,212,255,0.4); }
.acciones-right { display: flex; align-items: center; gap: 14px; }
.fecha-label { font-size: 13px; color: #7a96b0; }
.btn-guardar-asistencia { padding: 10px 20px; background: linear-gradient(135deg, #0077b6, #00b4d8); border: none; border-radius: 10px; color: white; font-family: 'Sora', sans-serif; font-size: 13px; font-weight: 600; cursor: pointer; transition: all 0.2s; }
.btn-guardar-asistencia:hover { box-shadow: 0 6px 20px rgba(0,180,216,0.35); }

/* Tabla */
.panel { background: #0a1628; border: 1px solid rgba(0,212,255,0.08); border-radius: 16px; overflow: hidden; margin-bottom: 16px; }
.tabla { width: 100%; border-collapse: collapse; }
.tabla thead tr { border-bottom: 1px solid rgba(0,212,255,0.08); }
.tabla th { padding: 13px 16px; text-align: left; font-size: 11px; font-weight: 600; color: #7a96b0; text-transform: uppercase; letter-spacing: 0.8px; }
.th-center { text-align: center !important; }
.tabla tbody tr { border-bottom: 1px solid rgba(255,255,255,0.04); transition: background 0.15s; }
.tabla tbody tr:last-child { border-bottom: none; }
.tabla tbody tr:hover { background: rgba(0,212,255,0.03); }
.tabla td { padding: 13px 16px; font-size: 13px; vertical-align: middle; }
.text-gris { color: #7a96b0; font-size: 12px; }

/* Estudiante cell */
.est-cell { display: flex; align-items: center; gap: 10px; }
.est-avatar { width: 34px; height: 34px; border-radius: 50%; background: linear-gradient(135deg, #0077b6, #a855f7); display: flex; align-items: center; justify-content: center; font-size: 11px; font-weight: 700; flex-shrink: 0; }
.est-cell strong { display: block; font-size: 13px; font-weight: 600; margin-bottom: 2px; }
.est-cell span { font-size: 11px; color: #7a96b0; }

/* Asistencia */
.asist-wrap { display: flex; align-items: center; gap: 8px; }
.asist-bar { width: 60px; height: 4px; background: rgba(255,255,255,0.06); border-radius: 4px; }
.asist-fill { height: 100%; border-radius: 4px; }
.ast-alta  .asist-fill, .ast-alta  { background: #22c55e; color: #22c55e; }
.ast-media .asist-fill, .ast-media { background: #fbbf24; color: #fbbf24; }
.ast-baja  .asist-fill, .ast-baja  { background: #ef4444; color: #ef4444; }
.asist-wrap span { font-size: 12px; font-weight: 600; width: 36px; }

/* Nota */
.nota { font-size: 15px; font-weight: 700; }
.nota-alta  { color: #22c55e; }
.nota-media { color: #fbbf24; }
.nota-baja  { color: #ef4444; }

/* Riesgo */
.badge-riesgo { font-size: 11px; font-weight: 600; padding: 4px 10px; border-radius: 100px; }
.badge-riesgo.ok    { background: rgba(34,197,94,0.1);  color: #22c55e; }
.badge-riesgo.medio { background: rgba(251,191,36,0.1); color: #fbbf24; }
.badge-riesgo.alto  { background: rgba(239,68,68,0.1);  color: #ef4444; }

/* Toggle asistencia */
.asist-toggle { display: flex; gap: 4px; justify-content: center; }
.toggle-btn { width: 30px; height: 30px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.1); background: transparent; color: #7a96b0; font-family: 'Sora', sans-serif; font-size: 12px; font-weight: 700; cursor: pointer; transition: all 0.2s; }
.toggle-btn.presente { background: rgba(34,197,94,0.2); border-color: rgba(34,197,94,0.4); color: #22c55e; }
.toggle-btn.ausente  { background: rgba(239,68,68,0.2);  border-color: rgba(239,68,68,0.4);  color: #ef4444; }

/* Resumen */
.resumen-hoy { display: flex; gap: 12px; }
.res-item { flex: 1; background: #0a1628; border: 1px solid rgba(0,212,255,0.08); border-radius: 12px; padding: 16px; text-align: center; }
.res-num { display: block; font-size: 28px; font-weight: 800; }
.res-label { font-size: 11px; color: #7a96b0; text-transform: uppercase; letter-spacing: 0.5px; }
.res-p .res-num { color: #22c55e; }
.res-a .res-num { color: #ef4444; }
.res-total .res-num { color: #00d4ff; }

/* Alerta */
.alert-success { margin-top: 16px; background: rgba(34,197,94,0.1); border: 1px solid rgba(34,197,94,0.25); color: #86efac; border-radius: 12px; padding: 14px 18px; font-size: 13px; font-weight: 500; }
</style>