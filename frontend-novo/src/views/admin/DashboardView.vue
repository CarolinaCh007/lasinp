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
          <h1>Panel de Administración</h1>
          <p>Gestión de pagos e inscripciones del LASIN</p>
        </div>
        <div class="top-date">{{ fechaHoy }}</div>
      </div>

      <!-- Cards resumen -->
      <div class="cards-grid">
        <div class="card card-cyan">
          <div class="card-icon">📋</div>
          <div class="card-info">
            <span class="card-num">12</span>
            <span class="card-label">Pendientes de pago</span>
          </div>
        </div>
        <div class="card card-green">
          <div class="card-icon">✅</div>
          <div class="card-info">
            <span class="card-num">87</span>
            <span class="card-label">Inscritos confirmados</span>
          </div>
        </div>
        <div class="card card-blue">
          <div class="card-icon">📚</div>
          <div class="card-info">
            <span class="card-num">8</span>
            <span class="card-label">Cursos activos</span>
          </div>
        </div>
        <div class="card card-gold">
          <div class="card-icon">💰</div>
          <div class="card-info">
            <span class="card-num">Bs. 34,200</span>
            <span class="card-label">Ingresos del mes</span>
          </div>
        </div>
      </div>

      <!-- Dos columnas -->
      <div class="two-col">

        <!-- Cursos activos -->
        <div class="panel">
          <div class="panel-header">
            <h2>📚 Cursos activos</h2>
            <router-link to="/admin/preinscritos" class="ver-mas">Ver preinscritos →</router-link>
          </div>
          <div class="curso-item" v-for="curso in cursos" :key="curso.id">
            <div class="curso-dot" :style="{ background: curso.color }"></div>
            <div class="curso-info">
              <strong>{{ curso.nombre }}</strong>
              <span>{{ curso.docente }}</span>
            </div>
            <div class="curso-stats">
              <span class="stat-inscritos">{{ curso.inscritos }} inscritos</span>
              <span class="stat-pendientes" v-if="curso.pendientes > 0">
                {{ curso.pendientes }} pendientes
              </span>
            </div>
          </div>
        </div>

        <!-- Últimas acciones -->
        <div class="panel">
          <div class="panel-header">
            <h2>🕐 Últimas confirmaciones</h2>
          </div>
          <div class="accion-item" v-for="a in acciones" :key="a.id">
            <div class="accion-avatar">{{ iniciales(a.estudiante) }}</div>
            <div class="accion-info">
              <strong>{{ a.estudiante }}</strong>
              <span>{{ a.curso }}</span>
            </div>
            <div class="accion-right">
              <span class="accion-monto">Bs. {{ a.monto }}</span>
              <span class="accion-time">{{ a.tiempo }}</span>
            </div>
          </div>
        </div>

      </div>

      <!-- Alertas pendientes -->
      <div class="panel mt" v-if="pendientesUrgentes.length > 0">
        <div class="panel-header">
          <h2>⚠️ Requieren atención</h2>
          <span class="badge-urgente">{{ pendientesUrgentes.length }} pendientes</span>
        </div>
        <div class="urgente-item" v-for="p in pendientesUrgentes" :key="p.id">
          <div class="urg-info">
            <strong>{{ p.estudiante }}</strong>
            <span>{{ p.curso }} · Preinscrito el {{ p.fecha }}</span>
          </div>
          <div class="urg-dias">
            <span class="dias-badge" :class="p.dias > 3 ? 'rojo' : 'amarillo'">
              {{ p.dias }} días esperando
            </span>
          </div>
          <button class="btn-confirmar" @click="confirmarPago(p)">
            ✓ Confirmar pago
          </button>
        </div>
      </div>

    </main>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const fechaHoy = computed(() =>
  new Date().toLocaleDateString('es-BO', {
    weekday: 'long', year: 'numeric', month: 'long', day: 'numeric'
  })
)

const cursos = ref([
  { id: 1, nombre: 'Python para Data Science',   docente: 'Lic. Mamani', inscritos: 28, pendientes: 3, color: '#00d4ff' },
  { id: 2, nombre: 'React & Angular Avanzado',    docente: 'Lic. Quispe',  inscritos: 22, pendientes: 2, color: '#a855f7' },
  { id: 3, nombre: 'Azure Fundamentals',          docente: 'Lic. Condori', inscritos: 15, pendientes: 4, color: '#0077b6' },
  { id: 4, nombre: 'Machine Learning Aplicado',   docente: 'Lic. Mamani', inscritos: 18, pendientes: 2, color: '#ffd700' },
  { id: 5, nombre: 'Excel & Power BI Avanzado',   docente: 'Lic. Flores',  inscritos: 24, pendientes: 1, color: '#22c55e' },
])

const acciones = ref([
  { id: 1, estudiante: 'Carolina Chávez', curso: 'Python Data Science',   monto: 350, tiempo: 'Hace 15min' },
  { id: 2, estudiante: 'Carlos Quispe',   curso: 'React & Angular',        monto: 400, tiempo: 'Hace 1h'   },
  { id: 3, estudiante: 'Ana Flores',      curso: 'Azure Fundamentals',     monto: 380, tiempo: 'Hace 2h'   },
  { id: 4, estudiante: 'Sofia Mamani',    curso: 'Machine Learning',       monto: 480, tiempo: 'Ayer'      },
])

const pendientesUrgentes = ref([
  { id: 1, estudiante: 'Juan Pérez',    curso: 'Python Data Science', fecha: '14/02/2025', dias: 5 },
  { id: 2, estudiante: 'Luis Condori',  curso: 'Azure Fundamentals',  fecha: '15/02/2025', dias: 4 },
  { id: 3, estudiante: 'María López',   curso: 'React & Angular',     fecha: '16/02/2025', dias: 3 },
])

function iniciales(nombre) {
  return nombre.split(' ').map(n => n[0]).join('').slice(0, 2).toUpperCase()
}

function confirmarPago(p) {
  pendientesUrgentes.value = pendientesUrgentes.value.filter(x => x.id !== p.id)
  acciones.value.unshift({
    id: Date.now(),
    estudiante: p.estudiante,
    curso: p.curso,
    monto: 350,
    tiempo: 'Ahora'
  })
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
.top-bar { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 28px; }
.top-bar h1 { font-size: 26px; font-weight: 700; margin-bottom: 4px; }
.top-bar p { font-size: 14px; color: #7a96b0; }
.top-date { font-size: 13px; color: #7a96b0; text-transform: capitalize; }

.cards-grid { display: grid; grid-template-columns: repeat(4,1fr); gap: 16px; margin-bottom: 24px; }
.card { border-radius: 16px; padding: 20px; display: flex; align-items: center; gap: 16px; border: 1px solid transparent; }
.card-cyan  { background: rgba(0,212,255,0.08);  border-color: rgba(0,212,255,0.2); }
.card-green { background: rgba(34,197,94,0.08);  border-color: rgba(34,197,94,0.2); }
.card-blue  { background: rgba(0,119,182,0.12);  border-color: rgba(0,119,182,0.25); }
.card-gold  { background: rgba(255,215,0,0.08);  border-color: rgba(255,215,0,0.2); }
.card-icon { font-size: 24px; }
.card-num   { display: block; font-size: 22px; font-weight: 800; }
.card-label { font-size: 11px; color: #7a96b0; text-transform: uppercase; letter-spacing: 0.5px; }
.card-cyan  .card-num { color: #00d4ff; }
.card-green .card-num { color: #22c55e; }
.card-blue  .card-num { color: #00b4d8; }
.card-gold  .card-num { color: #ffd700; font-size: 18px; }

.two-col { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 20px; }

.panel { background: #0a1628; border: 1px solid rgba(0,212,255,0.08); border-radius: 16px; overflow: hidden; }
.panel.mt { margin-top: 0; }
.panel-header { display: flex; justify-content: space-between; align-items: center; padding: 18px 20px; border-bottom: 1px solid rgba(0,212,255,0.08); }
.panel-header h2 { font-size: 15px; font-weight: 600; }
.ver-mas { font-size: 12px; color: #00d4ff; text-decoration: none; }
.badge-urgente { background: rgba(239,68,68,0.15); color: #f87171; font-size: 11px; font-weight: 600; padding: 3px 10px; border-radius: 100px; }

.curso-item { display: flex; align-items: center; gap: 12px; padding: 14px 20px; border-bottom: 1px solid rgba(255,255,255,0.04); }
.curso-item:last-child { border-bottom: none; }
.curso-dot { width: 8px; height: 8px; border-radius: 50%; flex-shrink: 0; }
.curso-info { flex: 1; }
.curso-info strong { display: block; font-size: 13px; font-weight: 600; margin-bottom: 3px; }
.curso-info span { font-size: 11px; color: #7a96b0; }
.curso-stats { display: flex; flex-direction: column; align-items: flex-end; gap: 4px; }
.stat-inscritos { font-size: 12px; color: #22c55e; font-weight: 600; }
.stat-pendientes { font-size: 11px; color: #fbbf24; }

.accion-item { display: flex; align-items: center; gap: 12px; padding: 13px 20px; border-bottom: 1px solid rgba(255,255,255,0.04); }
.accion-item:last-child { border-bottom: none; }
.accion-avatar { width: 34px; height: 34px; border-radius: 50%; background: linear-gradient(135deg, #0077b6, #00d4ff); display: flex; align-items: center; justify-content: center; font-size: 11px; font-weight: 700; flex-shrink: 0; }
.accion-info { flex: 1; }
.accion-info strong { display: block; font-size: 13px; font-weight: 600; margin-bottom: 2px; }
.accion-info span { font-size: 11px; color: #7a96b0; }
.accion-right { text-align: right; }
.accion-monto { display: block; font-size: 14px; font-weight: 700; color: #22c55e; }
.accion-time { font-size: 11px; color: #7a96b0; }

.urgente-item { display: flex; align-items: center; gap: 16px; padding: 14px 20px; border-bottom: 1px solid rgba(255,255,255,0.04); }
.urgente-item:last-child { border-bottom: none; }
.urg-info { flex: 1; }
.urg-info strong { display: block; font-size: 13px; font-weight: 600; margin-bottom: 3px; }
.urg-info span { font-size: 11px; color: #7a96b0; }
.dias-badge { font-size: 11px; font-weight: 600; padding: 4px 10px; border-radius: 100px; white-space: nowrap; }
.dias-badge.rojo { background: rgba(239,68,68,0.15); color: #f87171; }
.dias-badge.amarillo { background: rgba(251,191,36,0.15); color: #fbbf24; }
.btn-confirmar { padding: 9px 18px; background: linear-gradient(135deg, #0077b6, #00b4d8); border: none; border-radius: 10px; color: white; font-family: 'Sora', sans-serif; font-size: 12px; font-weight: 600; cursor: pointer; white-space: nowrap; transition: all 0.2s; }
.btn-confirmar:hover { box-shadow: 0 4px 16px rgba(0,180,216,0.35); }
</style>