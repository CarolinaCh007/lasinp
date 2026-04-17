<template>
  <div class="dashboard">

    <!-- Sidebar -->
    <aside class="sidebar">
      <div class="sidebar-logo">
        <div class="logo-box">L2</div>
        <div>
          <strong>LASIN</strong>
          <span>Sistema v2.0</span>
        </div>
      </div>

      <nav class="sidebar-nav">
        <router-link to="/estudiante/dashboard" class="nav-item active">
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
          <div>
            <strong>Carolina Ch.</strong>
            <span>Estudiante</span>
          </div>
        </div>
        <button class="btn-logout" @click="cerrarSesion">
          <svg width="16" height="16" fill="none" stroke="currentColor" stroke-width="1.8" viewBox="0 0 24 24"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/><polyline points="16 17 21 12 16 7"/><line x1="21" y1="12" x2="9" y2="12"/></svg>
          Salir
        </button>
      </div>
    </aside>

    <!-- Contenido principal -->
    <main class="main">

      <!-- Header -->
      <div class="top-bar">
        <div>
          <h1>¡Hola, Carolina! 👋</h1>
          <p>Aquí tienes el resumen de tu actividad académica en el LASIN.</p>
        </div>
        <div class="top-date">{{ fechaHoy }}</div>
      </div>

      <!-- Tarjetas de resumen -->
      <div class="cards-grid">
        <div class="card card-blue">
          <div class="card-icon">
            <svg width="22" height="22" fill="none" stroke="currentColor" stroke-width="1.8" viewBox="0 0 24 24"><path d="M12 2L2 7l10 5 10-5-10-5z"/><path d="M2 17l10 5 10-5"/><path d="M2 12l10 5 10-5"/></svg>
          </div>
          <div class="card-info">
            <span class="card-num">2</span>
            <span class="card-label">Cursos activos</span>
          </div>
        </div>
        <div class="card card-green">
          <div class="card-icon">
            <svg width="22" height="22" fill="none" stroke="currentColor" stroke-width="1.8" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>
          </div>
          <div class="card-info">
            <span class="card-num">5</span>
            <span class="card-label">Cursos completados</span>
          </div>
        </div>
        <div class="card card-yellow">
          <div class="card-icon">
            <svg width="22" height="22" fill="none" stroke="currentColor" stroke-width="1.8" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
          </div>
          <div class="card-info">
            <span class="card-num">1</span>
            <span class="card-label">Pendiente de pago</span>
          </div>
        </div>
        <div class="card card-purple">
          <div class="card-icon">
            <svg width="22" height="22" fill="none" stroke="currentColor" stroke-width="1.8" viewBox="0 0 24 24"><path d="M12 20h9"/><path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"/></svg>
          </div>
          <div class="card-info">
            <span class="card-num">87%</span>
            <span class="card-label">Promedio general</span>
          </div>
        </div>
      </div>

      <!-- Contenido en dos columnas -->
      <div class="two-col">

        <!-- Cursos activos -->
        <div class="panel">
          <div class="panel-header">
            <h2>Mis cursos activos</h2>
            <router-link to="/estudiante/cursos" class="ver-mas">Ver todos →</router-link>
          </div>

          <div class="curso-item" v-for="curso in cursosActivos" :key="curso.id">
            <div class="curso-color" :style="{ background: curso.color }"></div>
            <div class="curso-info">
              <strong>{{ curso.nombre }}</strong>
              <span>{{ curso.docente }}</span>
            </div>
            <div class="curso-progress">
              <div class="progress-bar">
                <div class="progress-fill" :style="{ width: curso.progreso + '%', background: curso.color }"></div>
              </div>
              <span class="progress-num">{{ curso.progreso }}%</span>
            </div>
          </div>
        </div>

        <!-- Recomendaciones IA -->
        <div class="panel">
          <div class="panel-header">
            <h2>✨ Recomendados para ti</h2>
            <span class="badge-ia">IA</span>
          </div>

          <div class="recomendacion" v-for="rec in recomendaciones" :key="rec.id">
            <div class="rec-icon" :style="{ background: rec.color }">{{ rec.icono }}</div>
            <div class="rec-info">
              <strong>{{ rec.nombre }}</strong>
              <span>{{ rec.motivo }}</span>
            </div>
            <button class="btn-inscribir">Ver</button>
          </div>
        </div>

      </div>

      <!-- Notificaciones -->
      <div class="panel mt">
        <div class="panel-header">
          <h2>🔔 Notificaciones recientes</h2>
        </div>
        <div class="notif" v-for="n in notificaciones" :key="n.id" :class="n.tipo">
          <div class="notif-dot"></div>
          <div class="notif-text">
            <strong>{{ n.titulo }}</strong>
            <span>{{ n.descripcion }}</span>
          </div>
          <span class="notif-time">{{ n.tiempo }}</span>
        </div>
      </div>

    </main>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

// Fecha de hoy formateada
const fechaHoy = computed(() => {
  return new Date().toLocaleDateString('es-BO', {
    weekday: 'long', year: 'numeric',
    month: 'long', day: 'numeric'
  })
})

// Datos de ejemplo — luego vienen de Flask
const cursosActivos = ref([
  { id: 1, nombre: 'Python para Data Science', docente: 'Lic. Mamani', progreso: 65, color: '#3b9eff' },
  { id: 2, nombre: 'React / Angular Avanzado', docente: 'Lic. Quispe', progreso: 40, color: '#a855f7' },
])

const recomendaciones = ref([
  { id: 1, nombre: 'Machine Learning Aplicado', motivo: 'Basado en tu curso de Python', icono: '🤖', color: 'rgba(59,158,255,0.15)' },
  { id: 2, nombre: 'Docker & DevOps', motivo: 'Popular en tu carrera', icono: '🐳', color: 'rgba(168,85,247,0.15)' },
  { id: 3, nombre: 'SQL + BigQuery', motivo: 'Complementa Data Science', icono: '🗄️', color: 'rgba(34,197,94,0.15)' },
])

const notificaciones = ref([
  { id: 1, tipo: 'info', titulo: 'Examen próximo', descripcion: 'Python Data Science — Parcial el viernes 21/02', tiempo: 'Hace 1h' },
  { id: 2, tipo: 'success', titulo: 'Preinscripción confirmada', descripcion: 'Tu pago fue verificado. Ya estás inscrito en React.', tiempo: 'Hace 3h' },
  { id: 3, tipo: 'warning', titulo: 'Encuesta pendiente', descripcion: 'Califica el curso de HTML/CSS que completaste.', tiempo: 'Ayer' },
])

function cerrarSesion() {
  router.push('/login')
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;500;600;700&display=swap');

* { box-sizing: border-box; margin: 0; padding: 0; }

.dashboard {
  font-family: 'Sora', sans-serif;
  display: flex; min-height: 100vh;
  background: #0d1b2e; color: #f8faff;
}

/* ── Sidebar ── */
.sidebar {
  width: 260px; flex-shrink: 0;
  background: rgba(255,255,255,0.03);
  border-right: 1px solid rgba(255,255,255,0.07);
  display: flex; flex-direction: column;
  padding: 28px 20px;
}
.sidebar-logo {
  display: flex; align-items: center; gap: 12px;
  margin-bottom: 40px; padding: 0 8px;
}
.logo-box {
  width: 40px; height: 40px;
  background: linear-gradient(135deg, #1d6fc4, #00d4ff);
  border-radius: 10px; display: flex;
  align-items: center; justify-content: center;
  font-size: 14px; font-weight: 700; color: white;
  flex-shrink: 0;
}
.sidebar-logo strong { display: block; font-size: 15px; font-weight: 700; }
.sidebar-logo span   { font-size: 11px; color: #8a9bb5; }

.sidebar-nav { display: flex; flex-direction: column; gap: 4px; flex: 1; }
.nav-item {
  display: flex; align-items: center; gap: 12px;
  padding: 11px 14px; border-radius: 10px;
  color: #8a9bb5; text-decoration: none;
  font-size: 14px; font-weight: 500;
  transition: all 0.2s;
}
.nav-item:hover { background: rgba(255,255,255,0.05); color: white; }
.nav-item.active { background: rgba(29,111,196,0.2); color: #00d4ff; }
.nav-item.router-link-active { background: rgba(29,111,196,0.2); color: #00d4ff; }

.sidebar-footer { border-top: 1px solid rgba(255,255,255,0.07); padding-top: 20px; }
.user-info {
  display: flex; align-items: center; gap: 10px; margin-bottom: 12px;
}
.user-avatar {
  width: 36px; height: 36px; border-radius: 50%;
  background: linear-gradient(135deg, #1d6fc4, #a855f7);
  display: flex; align-items: center; justify-content: center;
  font-size: 12px; font-weight: 700; flex-shrink: 0;
}
.user-info strong { display: block; font-size: 13px; }
.user-info span   { font-size: 11px; color: #8a9bb5; }
.btn-logout {
  width: 100%; display: flex; align-items: center; gap: 8px;
  padding: 9px 14px; background: transparent;
  border: 1px solid rgba(255,255,255,0.08);
  border-radius: 8px; color: #8a9bb5; font-family: 'Sora', sans-serif;
  font-size: 13px; cursor: pointer; transition: all 0.2s;
}
.btn-logout:hover { border-color: rgba(220,38,38,0.4); color: #fca5a5; }

/* ── Main ── */
.main { flex: 1; padding: 36px 40px; overflow-y: auto; }

.top-bar {
  display: flex; justify-content: space-between;
  align-items: flex-start; margin-bottom: 32px;
}
.top-bar h1 { font-size: 26px; font-weight: 700; margin-bottom: 4px; }
.top-bar p  { font-size: 14px; color: #8a9bb5; }
.top-date { font-size: 13px; color: #8a9bb5; text-transform: capitalize; }

/* Cards resumen */
.cards-grid {
  display: grid; grid-template-columns: repeat(4, 1fr);
  gap: 16px; margin-bottom: 28px;
}
.card {
  border-radius: 16px; padding: 20px;
  display: flex; align-items: center; gap: 16px;
  border: 1px solid transparent;
}
.card-blue   { background: rgba(59,158,255,0.1);  border-color: rgba(59,158,255,0.2); }
.card-green  { background: rgba(34,197,94,0.1);   border-color: rgba(34,197,94,0.2); }
.card-yellow { background: rgba(251,191,36,0.1);  border-color: rgba(251,191,36,0.2); }
.card-purple { background: rgba(168,85,247,0.1);  border-color: rgba(168,85,247,0.2); }
.card-icon { opacity: 0.8; }
.card-blue   .card-icon { color: #3b9eff; }
.card-green  .card-icon { color: #22c55e; }
.card-yellow .card-icon { color: #fbbf24; }
.card-purple .card-icon { color: #a855f7; }
.card-num   { display: block; font-size: 28px; font-weight: 700; line-height: 1; }
.card-label { font-size: 12px; color: #8a9bb5; margin-top: 4px; display: block; }

/* Dos columnas */
.two-col {
  display: grid; grid-template-columns: 1fr 1fr;
  gap: 20px; margin-bottom: 20px;
}
.mt { margin-top: 0; }

/* Panel */
.panel {
  background: rgba(255,255,255,0.03);
  border: 1px solid rgba(255,255,255,0.07);
  border-radius: 16px; padding: 24px;
}
.panel-header {
  display: flex; justify-content: space-between;
  align-items: center; margin-bottom: 20px;
}
.panel-header h2 { font-size: 15px; font-weight: 600; }
.ver-mas { font-size: 12px; color: #3b9eff; text-decoration: none; }
.ver-mas:hover { color: #00d4ff; }
.badge-ia {
  font-size: 10px; font-weight: 700; letter-spacing: 1px;
  background: linear-gradient(135deg, #1d6fc4, #a855f7);
  padding: 3px 8px; border-radius: 100px; color: white;
}

/* Cursos activos */
.curso-item {
  display: flex; align-items: center; gap: 14px;
  padding: 14px 0; border-bottom: 1px solid rgba(255,255,255,0.05);
}
.curso-item:last-child { border-bottom: none; padding-bottom: 0; }
.curso-color { width: 4px; height: 40px; border-radius: 4px; flex-shrink: 0; }
.curso-info { flex: 1; }
.curso-info strong { display: block; font-size: 13px; font-weight: 600; margin-bottom: 3px; }
.curso-info span   { font-size: 11px; color: #8a9bb5; }
.curso-progress { display: flex; align-items: center; gap: 10px; }
.progress-bar { width: 80px; height: 4px; background: rgba(255,255,255,0.08); border-radius: 4px; }
.progress-fill { height: 100%; border-radius: 4px; transition: width 0.8s ease; }
.progress-num { font-size: 12px; color: #8a9bb5; width: 30px; text-align: right; }

/* Recomendaciones */
.recomendacion {
  display: flex; align-items: center; gap: 14px;
  padding: 12px 0; border-bottom: 1px solid rgba(255,255,255,0.05);
}
.recomendacion:last-child { border-bottom: none; }
.rec-icon {
  width: 40px; height: 40px; border-radius: 10px;
  display: flex; align-items: center; justify-content: center;
  font-size: 18px; flex-shrink: 0;
}
.rec-info { flex: 1; }
.rec-info strong { display: block; font-size: 13px; font-weight: 600; margin-bottom: 3px; }
.rec-info span   { font-size: 11px; color: #8a9bb5; }
.btn-inscribir {
  padding: 6px 14px; background: rgba(29,111,196,0.2);
  border: 1px solid rgba(29,111,196,0.3);
  border-radius: 8px; color: #3b9eff;
  font-family: 'Sora', sans-serif; font-size: 12px;
  cursor: pointer; transition: all 0.2s; white-space: nowrap;
}
.btn-inscribir:hover { background: rgba(29,111,196,0.4); }

/* Notificaciones */
.notif {
  display: flex; align-items: flex-start; gap: 14px;
  padding: 14px 0; border-bottom: 1px solid rgba(255,255,255,0.05);
}
.notif:last-child { border-bottom: none; }
.notif-dot {
  width: 8px; height: 8px; border-radius: 50%;
  margin-top: 5px; flex-shrink: 0;
}
.notif.info    .notif-dot { background: #3b9eff; }
.notif.success .notif-dot { background: #22c55e; }
.notif.warning .notif-dot { background: #fbbf24; }
.notif-text { flex: 1; }
.notif-text strong { display: block; font-size: 13px; font-weight: 600; margin-bottom: 3px; }
.notif-text span   { font-size: 12px; color: #8a9bb5; }
.notif-time { font-size: 11px; color: #8a9bb5; white-space: nowrap; }
</style>