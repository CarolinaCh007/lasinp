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
        <router-link to="/docente/dashboard" class="nav-item">
          <svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="1.8" viewBox="0 0 24 24"><rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/></svg>
          Dashboard
        </router-link>
        <router-link to="/docente/estudiantes" class="nav-item">
          <svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="1.8" viewBox="0 0 24 24"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>
          Mis Estudiantes
        </router-link>
        <router-link to="/docente/calificaciones" class="nav-item">
          <svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="1.8" viewBox="0 0 24 24"><path d="M12 20h9"/><path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"/></svg>
          Calificaciones
        </router-link>
        <router-link to="/docente/comunicados" class="nav-item">
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
          <h1>¡Hola, Lic. Mamani! 👨‍🏫</h1>
          <p>Resumen de tu actividad docente en el LASIN</p>
        </div>
        <div class="top-date">{{ fechaHoy }}</div>
      </div>

      <!-- Cards resumen -->
      <div class="cards-grid">
        <div class="card card-blue">
          <div class="card-icon">📚</div>
          <div class="card-info">
            <span class="card-num">3</span>
            <span class="card-label">Cursos activos</span>
          </div>
        </div>
        <div class="card card-cyan">
          <div class="card-icon">👥</div>
          <div class="card-info">
            <span class="card-num">67</span>
            <span class="card-label">Estudiantes</span>
          </div>
        </div>
        <div class="card card-gold">
          <div class="card-icon">📊</div>
          <div class="card-info">
            <span class="card-num">81%</span>
            <span class="card-label">Promedio grupo</span>
          </div>
        </div>
        <div class="card card-green">
          <div class="card-icon">✅</div>
          <div class="card-info">
            <span class="card-num">89%</span>
            <span class="card-label">Asistencia media</span>
          </div>
        </div>
      </div>

      <!-- Dos columnas -->
      <div class="two-col">

        <!-- Mis cursos -->
        <div class="panel">
          <div class="panel-header">
            <h2>Mis cursos activos</h2>
          </div>
          <div class="curso-item" v-for="curso in cursos" :key="curso.id">
            <div class="curso-color" :style="{ background: curso.color }"></div>
            <div class="curso-info">
              <strong>{{ curso.nombre }}</strong>
              <span>{{ curso.inscritos }} estudiantes · {{ curso.horario }}</span>
            </div>
            <div class="curso-right">
              <span class="curso-pct">{{ curso.progreso }}%</span>
              <div class="mini-bar">
                <div class="mini-fill" :style="{ width: curso.progreso + '%', background: curso.color }"></div>
              </div>
            </div>
          </div>
        </div>

        <!-- Agenda de hoy -->
        <div class="panel">
          <div class="panel-header">
            <h2>📅 Agenda de hoy</h2>
          </div>
          <div class="agenda-item" v-for="item in agenda" :key="item.id" :class="item.tipo">
            <div class="agenda-hora">{{ item.hora }}</div>
            <div class="agenda-info">
              <strong>{{ item.titulo }}</strong>
              <span>{{ item.lugar }}</span>
            </div>
            <div class="agenda-badge" :class="item.tipo">{{ item.tipo }}</div>
          </div>
          <div class="sin-agenda" v-if="agenda.length === 0">
            <p>No tienes actividades programadas para hoy.</p>
          </div>
        </div>

      </div>

      <!-- Actividad reciente -->
      <div class="panel mt">
        <div class="panel-header">
          <h2>🔔 Actividad reciente</h2>
        </div>
        <div class="actividad" v-for="a in actividades" :key="a.id">
          <div class="act-dot" :class="a.tipo"></div>
          <div class="act-info">
            <strong>{{ a.titulo }}</strong>
            <span>{{ a.desc }}</span>
          </div>
          <span class="act-time">{{ a.tiempo }}</span>
        </div>
      </div>

    </main>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const fechaHoy = computed(() =>
  new Date().toLocaleDateString('es-BO', {
    weekday: 'long', year: 'numeric',
    month: 'long', day: 'numeric'
  })
)

const cursos = ref([
  { id: 1, nombre: 'Python para Data Science', inscritos: 28, horario: 'Lun/Mié 08:00–10:00', progreso: 65, color: 'linear-gradient(90deg,#0077b6,#00d4ff)' },
  { id: 2, nombre: 'Machine Learning Aplicado', inscritos: 22, horario: 'Mar/Jue 10:00–12:00', progreso: 40, color: 'linear-gradient(90deg,#7c3aed,#a855f7)' },
  { id: 3, nombre: 'Intro a la Inteligencia Artificial', inscritos: 17, horario: 'Vie 14:00–17:00', progreso: 20, color: 'linear-gradient(90deg,#ffd700,#f59e0b)' },
])

const agenda = ref([
  { id: 1, hora: '08:00', titulo: 'Python para Data Science', lugar: 'Lab 3 · LASIN', tipo: 'clase' },
  { id: 2, hora: '12:00', titulo: 'Entrega de calificaciones parciales', lugar: 'Sistema LASIN', tipo: 'tarea' },
  { id: 3, hora: '14:00', titulo: 'Reunión docentes LASIN', lugar: 'Sala de reuniones', tipo: 'reunion' },
])

const actividades = ref([
  { id: 1, tipo: 'info',    titulo: '3 nuevos preinscritos',        desc: 'Machine Learning Aplicado tiene 3 solicitudes pendientes.',  tiempo: 'Hace 30min' },
  { id: 2, tipo: 'success', titulo: 'Asistencia registrada',        desc: 'Python Data Science · Clase del 18/02.',                    tiempo: 'Hace 2h' },
  { id: 3, tipo: 'warning', titulo: '2 estudiantes con bajo rendimiento', desc: 'Revisar historial de Juan P. y María L.',              tiempo: 'Ayer' },
  { id: 4, tipo: 'info',    titulo: 'Comunicado enviado',           desc: 'Recordatorio de examen parcial enviado a 28 estudiantes.',   tiempo: 'Ayer' },
])
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
.top-bar { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 28px; }
.top-bar h1 { font-size: 26px; font-weight: 700; margin-bottom: 4px; }
.top-bar p { font-size: 14px; color: #7a96b0; }
.top-date { font-size: 13px; color: #7a96b0; text-transform: capitalize; }

/* Cards */
.cards-grid { display: grid; grid-template-columns: repeat(4,1fr); gap: 16px; margin-bottom: 24px; }
.card { border-radius: 16px; padding: 20px; display: flex; align-items: center; gap: 16px; border: 1px solid transparent; }
.card-blue  { background: rgba(0,119,182,0.12);  border-color: rgba(0,119,182,0.25); }
.card-cyan  { background: rgba(0,212,255,0.08);  border-color: rgba(0,212,255,0.2); }
.card-gold  { background: rgba(255,215,0,0.08);  border-color: rgba(255,215,0,0.2); }
.card-green { background: rgba(34,197,94,0.08);  border-color: rgba(34,197,94,0.2); }
.card-icon { font-size: 24px; }
.card-num   { display: block; font-size: 26px; font-weight: 800; }
.card-label { font-size: 11px; color: #7a96b0; text-transform: uppercase; letter-spacing: 0.5px; }
.card-blue  .card-num { color: #00b4d8; }
.card-cyan  .card-num { color: #00d4ff; }
.card-gold  .card-num { color: #ffd700; }
.card-green .card-num { color: #22c55e; }

/* Dos columnas */
.two-col { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 20px; }

/* Panel */
.panel { background: #0a1628; border: 1px solid rgba(0,212,255,0.08); border-radius: 16px; padding: 22px; }
.panel.mt { margin-top: 0; }
.panel-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 18px; }
.panel-header h2 { font-size: 15px; font-weight: 600; }

/* Cursos */
.curso-item { display: flex; align-items: center; gap: 12px; padding: 13px 0; border-bottom: 1px solid rgba(255,255,255,0.04); }
.curso-item:last-child { border-bottom: none; }
.curso-color { width: 4px; height: 40px; border-radius: 4px; flex-shrink: 0; }
.curso-info { flex: 1; }
.curso-info strong { display: block; font-size: 13px; font-weight: 600; margin-bottom: 3px; }
.curso-info span { font-size: 11px; color: #7a96b0; }
.curso-right { text-align: right; }
.curso-pct { font-size: 13px; font-weight: 700; color: #00d4ff; display: block; margin-bottom: 5px; }
.mini-bar { width: 80px; height: 4px; background: rgba(255,255,255,0.06); border-radius: 4px; }
.mini-fill { height: 100%; border-radius: 4px; }

/* Agenda */
.agenda-item { display: flex; align-items: center; gap: 14px; padding: 12px 0; border-bottom: 1px solid rgba(255,255,255,0.04); }
.agenda-item:last-child { border-bottom: none; }
.agenda-hora { font-size: 13px; font-weight: 700; color: #00d4ff; width: 48px; flex-shrink: 0; }
.agenda-info { flex: 1; }
.agenda-info strong { display: block; font-size: 13px; font-weight: 600; margin-bottom: 2px; }
.agenda-info span { font-size: 11px; color: #7a96b0; }
.agenda-badge { font-size: 10px; font-weight: 600; padding: 3px 10px; border-radius: 100px; text-transform: capitalize; }
.agenda-badge.clase   { background: rgba(0,119,182,0.2);  color: #00d4ff; }
.agenda-badge.tarea   { background: rgba(255,215,0,0.15); color: #ffd700; }
.agenda-badge.reunion { background: rgba(168,85,247,0.15);color: #a855f7; }
.sin-agenda { text-align: center; padding: 24px; color: #7a96b0; font-size: 13px; }

/* Actividades */
.actividad { display: flex; align-items: flex-start; gap: 14px; padding: 13px 0; border-bottom: 1px solid rgba(255,255,255,0.04); }
.actividad:last-child { border-bottom: none; }
.act-dot { width: 8px; height: 8px; border-radius: 50%; margin-top: 5px; flex-shrink: 0; }
.act-dot.info    { background: #00d4ff; }
.act-dot.success { background: #22c55e; }
.act-dot.warning { background: #ffd700; }
.act-info { flex: 1; }
.act-info strong { display: block; font-size: 13px; font-weight: 600; margin-bottom: 3px; }
.act-info span { font-size: 12px; color: #7a96b0; }
.act-time { font-size: 11px; color: #7a96b0; white-space: nowrap; }
</style>