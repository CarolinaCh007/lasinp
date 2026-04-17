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
        <router-link to="/superadmin/usuarios"  class="nav-item">
          <svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="1.8" viewBox="0 0 24 24"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>
          Usuarios
        </router-link>
        <router-link to="/superadmin/cursos"    class="nav-item">
          <svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="1.8" viewBox="0 0 24 24"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/></svg>
          Cursos
        </router-link>
        <router-link to="/superadmin/reportes"  class="nav-item">
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
          <h1>Dashboard Ejecutivo ⚙️</h1>
          <p>Vista general del sistema LASIN 2.0 — {{ fechaHoy }}</p>
        </div>
        <div class="top-badges">
          <span class="badge-sistema">🟢 Sistema operativo</span>
          <span class="badge-version">v2.0.0</span>
        </div>
      </div>

      <!-- KPIs principales -->
      <div class="kpis-grid">
        <div class="kpi" v-for="k in kpis" :key="k.label">
          <div class="kpi-icon" :style="{ background: k.bg }">{{ k.icono }}</div>
          <div class="kpi-info">
            <span class="kpi-num" :style="{ color: k.color }">{{ k.valor }}</span>
            <span class="kpi-label">{{ k.label }}</span>
            <span class="kpi-trend" :class="k.trend > 0 ? 'up' : 'down'">
              {{ k.trend > 0 ? '↑' : '↓' }} {{ Math.abs(k.trend) }}% vs mes anterior
            </span>
          </div>
        </div>
      </div>

      <!-- Tres columnas -->
      <div class="three-col">

        <!-- Usuarios por rol -->
        <div class="panel">
          <div class="panel-header">
            <h2>👥 Usuarios por rol</h2>
            <router-link to="/superadmin/usuarios" class="ver-mas">Gestionar →</router-link>
          </div>
          <div class="rol-item" v-for="r in roles" :key="r.nombre">
            <div class="rol-icon" :style="{ background: r.bg }">{{ r.icono }}</div>
            <div class="rol-info">
              <strong>{{ r.nombre }}</strong>
              <div class="rol-bar">
                <div class="rol-fill" :style="{ width: (r.total / maxRol * 100) + '%', background: r.color }"></div>
              </div>
            </div>
            <span class="rol-num" :style="{ color: r.color }">{{ r.total }}</span>
          </div>
        </div>

        <!-- Cursos activos -->
        <div class="panel">
          <div class="panel-header">
            <h2>📚 Estado de cursos</h2>
            <router-link to="/superadmin/cursos" class="ver-mas">Gestionar →</router-link>
          </div>
          <div class="curso-estado" v-for="c in cursosEstado" :key="c.nombre">
            <div class="ce-dot" :style="{ background: c.color }"></div>
            <div class="ce-info">
              <strong>{{ c.nombre }}</strong>
              <span>{{ c.inscritos }}/{{ c.cupo }} inscritos</span>
            </div>
            <span class="ce-badge" :class="c.estado">{{ c.estado }}</span>
          </div>
        </div>

        <!-- Actividad del sistema -->
        <div class="panel">
          <div class="panel-header">
            <h2>🖥️ Sistema</h2>
          </div>
          <div class="sistema-item" v-for="s in sistema" :key="s.label">
            <div class="sis-label">
              <span>{{ s.icono }} {{ s.label }}</span>
              <span class="sis-val" :class="s.clase">{{ s.valor }}</span>
            </div>
            <div class="sis-bar" v-if="s.pct !== undefined">
              <div class="sis-fill" :style="{ width: s.pct + '%' }" :class="s.clase"></div>
            </div>
          </div>
        </div>

      </div>

      <!-- Actividad reciente -->
      <div class="panel">
        <div class="panel-header">
          <h2>🔔 Actividad reciente del sistema</h2>
          <router-link to="/superadmin/auditoria" class="ver-mas">Ver log completo →</router-link>
        </div>
        <div class="log-item" v-for="log in logs" :key="log.id">
          <div class="log-dot" :class="log.tipo"></div>
          <div class="log-info">
            <strong>{{ log.accion }}</strong>
            <span>{{ log.usuario }} · {{ log.detalle }}</span>
          </div>
          <span class="log-time">{{ log.tiempo }}</span>
        </div>
      </div>

    </main>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const fechaHoy = computed(() =>
  new Date().toLocaleDateString('es-BO', {
    weekday: 'long', year: 'numeric', month: 'long', day: 'numeric'
  })
)

const kpis = ref([
  { icono: '👥', label: 'Total usuarios',      valor: '312',        color: '#00d4ff', bg: 'rgba(0,212,255,0.12)',  trend: 12  },
  { icono: '📚', label: 'Cursos activos',       valor: '8',          color: '#ffd700', bg: 'rgba(255,215,0,0.12)', trend: 2   },
  { icono: '💰', label: 'Ingresos del mes',     valor: 'Bs. 34,200', color: '#22c55e', bg: 'rgba(34,197,94,0.12)', trend: 8   },
  { icono: '🎓', label: 'Inscritos activos',    valor: '99',         color: '#a855f7', bg: 'rgba(168,85,247,0.12)',trend: 15  },
  { icono: '⏳', label: 'Pendientes de pago',   valor: '12',         color: '#fbbf24', bg: 'rgba(251,191,36,0.12)',trend: -3  },
  { icono: '📊', label: 'Promedio general',     valor: '81%',        color: '#00b4d8', bg: 'rgba(0,180,216,0.12)', trend: 4   },
])

const roles = ref([
  { nombre: 'Estudiantes', icono: '🎓', total: 285, color: '#00d4ff', bg: 'rgba(0,212,255,0.12)' },
  { nombre: 'Docentes',    icono: '👨‍🏫', total: 12,  color: '#ffd700', bg: 'rgba(255,215,0,0.12)' },
  { nombre: 'Admins',      icono: '🗂️', total: 3,   color: '#22c55e', bg: 'rgba(34,197,94,0.12)' },
  { nombre: 'Super Admin', icono: '⚙️', total: 2,   color: '#a855f7', bg: 'rgba(168,85,247,0.12)' },
])

const maxRol = computed(() => Math.max(...roles.value.map(r => r.total)))

const cursosEstado = ref([
  { nombre: 'Python Data Science',  inscritos: 28, cupo: 30, estado: 'activo',  color: '#00d4ff' },
  { nombre: 'React & Angular',       inscritos: 22, cupo: 25, estado: 'activo',  color: '#a855f7' },
  { nombre: 'Azure Fundamentals',    inscritos: 15, cupo: 20, estado: 'activo',  color: '#0077b6' },
  { nombre: 'Machine Learning',      inscritos: 18, cupo: 20, estado: 'activo',  color: '#ffd700' },
  { nombre: 'Ethical Hacking',       inscritos: 20, cupo: 20, estado: 'lleno',   color: '#ef4444' },
  { nombre: 'Excel & Power BI',      inscritos: 16, cupo: 20, estado: 'activo',  color: '#22c55e' },
])

const sistema = ref([
  { icono: '🖥️', label: 'Servidor',       valor: 'Online',  clase: 'ok',      pct: undefined },
  { icono: '🗄️', label: 'Base de datos',  valor: '68%',     clase: 'ok',      pct: 68 },
  { icono: '💾', label: 'Almacenamiento', valor: '42%',     clase: 'ok',      pct: 42 },
  { icono: '⚡', label: 'CPU',            valor: '23%',     clase: 'ok',      pct: 23 },
  { icono: '🔐', label: 'Último backup',  valor: 'Hoy 03:00', clase: 'ok',    pct: undefined },
])

const logs = ref([
  { id: 1, tipo: 'success', accion: 'Inscripción confirmada',   usuario: 'Admin',         detalle: 'Carolina Chávez → Python Data Science',  tiempo: 'Hace 5min'  },
  { id: 2, tipo: 'info',    accion: 'Usuario creado',           usuario: 'Super Admin',   detalle: 'Nuevo docente: Lic. Rodríguez',            tiempo: 'Hace 20min' },
  { id: 3, tipo: 'warning', accion: 'Intento de login fallido', usuario: 'Desconocido',   detalle: 'IP: 190.129.45.12 · 3 intentos',          tiempo: 'Hace 1h'    },
  { id: 4, tipo: 'info',    accion: 'Curso creado',             usuario: 'Super Admin',   detalle: 'Docker & Kubernetes — Cupo: 20',           tiempo: 'Hace 2h'    },
  { id: 5, tipo: 'success', accion: 'Backup completado',        usuario: 'Sistema',       detalle: 'Backup automático ejecutado correctamente', tiempo: 'Hace 3h'    },
])
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
.user-avatar { width: 36px; height: 36px; border-radius: 50%; background: linear-gradient(135deg, #a855f7, #0077b6); display: flex; align-items: center; justify-content: center; font-size: 12px; font-weight: 700; flex-shrink: 0; }
.user-info strong { display: block; font-size: 13px; }
.user-info span { font-size: 11px; color: #7a96b0; }
.btn-logout { width: 100%; display: flex; align-items: center; gap: 8px; padding: 9px 14px; background: transparent; border: 1px solid rgba(255,255,255,0.07); border-radius: 8px; color: #7a96b0; font-family: 'Sora', sans-serif; font-size: 13px; cursor: pointer; transition: all 0.2s; }
.btn-logout:hover { border-color: rgba(239,68,68,0.4); color: #fca5a5; }

.main { flex: 1; padding: 36px 40px; overflow-y: auto; }
.top-bar { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 28px; }
.top-bar h1 { font-size: 26px; font-weight: 700; margin-bottom: 4px; }
.top-bar p { font-size: 14px; color: #7a96b0; text-transform: capitalize; }
.top-badges { display: flex; gap: 8px; align-items: center; }
.badge-sistema { font-size: 12px; background: rgba(34,197,94,0.12); border: 1px solid rgba(34,197,94,0.25); color: #22c55e; padding: 6px 14px; border-radius: 100px; font-weight: 500; }
.badge-version { font-size: 12px; background: rgba(0,212,255,0.1); border: 1px solid rgba(0,212,255,0.2); color: #00d4ff; padding: 6px 14px; border-radius: 100px; font-weight: 600; }

/* KPIs */
.kpis-grid { display: grid; grid-template-columns: repeat(6,1fr); gap: 14px; margin-bottom: 24px; }
.kpi { background: #0a1628; border: 1px solid rgba(0,212,255,0.08); border-radius: 16px; padding: 18px; display: flex; align-items: center; gap: 14px; }
.kpi-icon { width: 44px; height: 44px; border-radius: 12px; display: flex; align-items: center; justify-content: center; font-size: 20px; flex-shrink: 0; }
.kpi-num { display: block; font-size: 18px; font-weight: 800; line-height: 1; margin-bottom: 3px; }
.kpi-label { display: block; font-size: 10px; color: #7a96b0; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 4px; }
.kpi-trend { display: block; font-size: 10px; font-weight: 600; }
.kpi-trend.up   { color: #22c55e; }
.kpi-trend.down { color: #ef4444; }

/* Tres columnas */
.three-col { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 20px; margin-bottom: 20px; }

.panel { background: #0a1628; border: 1px solid rgba(0,212,255,0.08); border-radius: 16px; overflow: hidden; margin-bottom: 20px; }
.panel:last-child { margin-bottom: 0; }
.panel-header { display: flex; justify-content: space-between; align-items: center; padding: 18px 20px; border-bottom: 1px solid rgba(0,212,255,0.08); }
.panel-header h2 { font-size: 15px; font-weight: 600; }
.ver-mas { font-size: 12px; color: #00d4ff; text-decoration: none; }

/* Roles */
.rol-item { display: flex; align-items: center; gap: 12px; padding: 13px 20px; border-bottom: 1px solid rgba(255,255,255,0.04); }
.rol-item:last-child { border-bottom: none; }
.rol-icon { width: 34px; height: 34px; border-radius: 10px; display: flex; align-items: center; justify-content: center; font-size: 16px; flex-shrink: 0; }
.rol-info { flex: 1; }
.rol-info strong { display: block; font-size: 13px; font-weight: 600; margin-bottom: 6px; }
.rol-bar { height: 4px; background: rgba(255,255,255,0.06); border-radius: 4px; }
.rol-fill { height: 100%; border-radius: 4px; transition: width 1s ease; }
.rol-num { font-size: 16px; font-weight: 800; }

/* Cursos estado */
.curso-estado { display: flex; align-items: center; gap: 12px; padding: 12px 20px; border-bottom: 1px solid rgba(255,255,255,0.04); }
.curso-estado:last-child { border-bottom: none; }
.ce-dot { width: 8px; height: 8px; border-radius: 50%; flex-shrink: 0; }
.ce-info { flex: 1; }
.ce-info strong { display: block; font-size: 12px; font-weight: 600; margin-bottom: 2px; }
.ce-info span { font-size: 11px; color: #7a96b0; }
.ce-badge { font-size: 10px; font-weight: 600; padding: 3px 8px; border-radius: 100px; }
.ce-badge.activo { background: rgba(34,197,94,0.12); color: #22c55e; }
.ce-badge.lleno  { background: rgba(239,68,68,0.12);  color: #f87171; }
.ce-badge.proximo { background: rgba(251,191,36,0.12); color: #fbbf24; }

/* Sistema */
.sistema-item { padding: 12px 20px; border-bottom: 1px solid rgba(255,255,255,0.04); }
.sistema-item:last-child { border-bottom: none; }
.sis-label { display: flex; justify-content: space-between; font-size: 12px; margin-bottom: 6px; }
.sis-val { font-weight: 600; }
.sis-val.ok { color: #22c55e; }
.sis-val.warning { color: #fbbf24; }
.sis-bar { height: 4px; background: rgba(255,255,255,0.06); border-radius: 4px; }
.sis-fill { height: 100%; border-radius: 4px; }
.sis-fill.ok { background: #22c55e; }
.sis-fill.warning { background: #fbbf24; }

/* Logs */
.log-item { display: flex; align-items: flex-start; gap: 14px; padding: 13px 20px; border-bottom: 1px solid rgba(255,255,255,0.04); }
.log-item:last-child { border-bottom: none; }
.log-dot { width: 8px; height: 8px; border-radius: 50%; margin-top: 5px; flex-shrink: 0; }
.log-dot.success { background: #22c55e; }
.log-dot.info    { background: #00d4ff; }
.log-dot.warning { background: #fbbf24; }
.log-dot.error   { background: #ef4444; }
.log-info { flex: 1; }
.log-info strong { display: block; font-size: 13px; font-weight: 600; margin-bottom: 3px; }
.log-info span { font-size: 12px; color: #7a96b0; }
.log-time { font-size: 11px; color: #7a96b0; white-space: nowrap; }
</style>