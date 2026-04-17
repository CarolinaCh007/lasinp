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
          <h1>Reportes</h1>
          <p>Resumen de inscripciones e ingresos del LASIN</p>
        </div>
        <button class="btn-exportar">📄 Exportar PDF</button>
      </div>

      <!-- Cards resumen -->
      <div class="cards-grid">
        <div class="card card-cyan">
          <span class="card-icon">👥</span>
          <div>
            <span class="card-num">99</span>
            <span class="card-label">Total inscritos</span>
          </div>
        </div>
        <div class="card card-green">
          <span class="card-icon">💰</span>
          <div>
            <span class="card-num">Bs. 34,200</span>
            <span class="card-label">Ingresos del mes</span>
          </div>
        </div>
        <div class="card card-gold">
          <span class="card-icon">📚</span>
          <div>
            <span class="card-num">8</span>
            <span class="card-label">Cursos activos</span>
          </div>
        </div>
        <div class="card card-blue">
          <span class="card-icon">⏳</span>
          <div>
            <span class="card-num">12</span>
            <span class="card-label">Pendientes de pago</span>
          </div>
        </div>
      </div>

      <!-- Gráficas simuladas -->
      <div class="two-col">

        <!-- Inscritos por curso -->
        <div class="panel">
          <div class="panel-header">
            <h2>📊 Inscritos por curso</h2>
          </div>
          <div class="barra-item" v-for="c in cursos" :key="c.id">
            <div class="barra-label">
              <span>{{ c.nombre }}</span>
              <span class="barra-num">{{ c.inscritos }}</span>
            </div>
            <div class="barra-track">
              <div
                class="barra-fill"
                :style="{ width: (c.inscritos / maxInscritos * 100) + '%', background: c.color }"
              ></div>
            </div>
          </div>
        </div>

        <!-- Ingresos por curso -->
        <div class="panel">
          <div class="panel-header">
            <h2>💰 Ingresos por curso</h2>
          </div>
          <div class="barra-item" v-for="c in cursos" :key="c.id">
            <div class="barra-label">
              <span>{{ c.nombre }}</span>
              <span class="barra-num">Bs. {{ c.ingresos.toLocaleString() }}</span>
            </div>
            <div class="barra-track">
              <div
                class="barra-fill"
                :style="{ width: (c.ingresos / maxIngresos * 100) + '%', background: c.color }"
              ></div>
            </div>
          </div>
        </div>

      </div>

      <!-- Tabla detalle -->
      <div class="panel">
        <div class="panel-header">
          <h2>📋 Detalle por curso</h2>
        </div>
        <table class="tabla">
          <thead>
            <tr>
              <th>Curso</th>
              <th>Docente</th>
              <th class="th-center">Inscritos</th>
              <th class="th-center">Pendientes</th>
              <th class="th-center">Aprobados</th>
              <th class="th-right">Ingresos</th>
              <th class="th-center">Ocupación</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="c in cursos" :key="c.id">
              <td>
                <div class="curso-cell">
                  <div class="curso-dot" :style="{ background: c.color }"></div>
                  <strong>{{ c.nombre }}</strong>
                </div>
              </td>
              <td class="text-gris">{{ c.docente }}</td>
              <td class="th-center"><span class="num-cyan">{{ c.inscritos }}</span></td>
              <td class="th-center"><span class="num-yellow">{{ c.pendientes }}</span></td>
              <td class="th-center"><span class="num-green">{{ c.aprobados }}</span></td>
              <td class="th-right"><strong>Bs. {{ c.ingresos.toLocaleString() }}</strong></td>
              <td class="th-center">
                <div class="ocupacion-wrap">
                  <div class="ocup-bar">
                    <div
                      class="ocup-fill"
                      :style="{ width: (c.inscritos / c.cupoMax * 100) + '%', background: c.color }"
                    ></div>
                  </div>
                  <span>{{ Math.round(c.inscritos / c.cupoMax * 100) }}%</span>
                </div>
              </td>
            </tr>
          </tbody>
          <tfoot>
            <tr class="fila-total">
              <td colspan="2"><strong>TOTAL</strong></td>
              <td class="th-center"><strong class="num-cyan">{{ totalInscritos }}</strong></td>
              <td class="th-center"><strong class="num-yellow">{{ totalPendientes }}</strong></td>
              <td class="th-center"><strong class="num-green">{{ totalAprobados }}</strong></td>
              <td class="th-right"><strong>Bs. {{ totalIngresos.toLocaleString() }}</strong></td>
              <td></td>
            </tr>
          </tfoot>
        </table>
      </div>

    </main>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const cursos = ref([
  { id: 1, nombre: 'Python Data Science', docente: 'Lic. Mamani', inscritos: 28, pendientes: 3, aprobados: 0, cupoMax: 30, ingresos: 9800, color: '#00d4ff' },
  { id: 2, nombre: 'React & Angular',      docente: 'Lic. Quispe',  inscritos: 22, pendientes: 2, aprobados: 0, cupoMax: 25, ingresos: 8800, color: '#a855f7' },
  { id: 3, nombre: 'Azure Fundamentals',   docente: 'Lic. Condori', inscritos: 15, pendientes: 4, aprobados: 0, cupoMax: 20, ingresos: 5700, color: '#0077b6' },
  { id: 4, nombre: 'Machine Learning',     docente: 'Lic. Mamani', inscritos: 18, pendientes: 2, aprobados: 0, cupoMax: 20, ingresos: 8640, color: '#ffd700' },
  { id: 5, nombre: 'Excel & Power BI',     docente: 'Lic. Flores',  inscritos: 16, pendientes: 1, aprobados: 0, cupoMax: 20, ingresos: 4000, color: '#22c55e' },
])

const maxInscritos = computed(() => Math.max(...cursos.value.map(c => c.inscritos)))
const maxIngresos  = computed(() => Math.max(...cursos.value.map(c => c.ingresos)))
const totalInscritos  = computed(() => cursos.value.reduce((s, c) => s + c.inscritos, 0))
const totalPendientes = computed(() => cursos.value.reduce((s, c) => s + c.pendientes, 0))
const totalAprobados  = computed(() => cursos.value.reduce((s, c) => s + c.aprobados, 0))
const totalIngresos   = computed(() => cursos.value.reduce((s, c) => s + c.ingresos, 0))
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
.btn-exportar { padding: 10px 20px; background: rgba(255,215,0,0.1); border: 1px solid rgba(255,215,0,0.25); border-radius: 10px; color: #ffd700; font-family: 'Sora', sans-serif; font-size: 13px; font-weight: 600; cursor: pointer; }
.btn-exportar:hover { background: rgba(255,215,0,0.18); }

.cards-grid { display: grid; grid-template-columns: repeat(4,1fr); gap: 16px; margin-bottom: 24px; }
.card { border-radius: 16px; padding: 20px; display: flex; align-items: center; gap: 16px; border: 1px solid transparent; }
.card-cyan  { background: rgba(0,212,255,0.08);  border-color: rgba(0,212,255,0.2); }
.card-green { background: rgba(34,197,94,0.08);  border-color: rgba(34,197,94,0.2); }
.card-gold  { background: rgba(255,215,0,0.08);  border-color: rgba(255,215,0,0.2); }
.card-blue  { background: rgba(0,119,182,0.12);  border-color: rgba(0,119,182,0.25); }
.card-icon { font-size: 24px; }
.card-num  { display: block; font-size: 20px; font-weight: 800; }
.card-label { font-size: 11px; color: #7a96b0; text-transform: uppercase; letter-spacing: 0.5px; }
.card-cyan  .card-num { color: #00d4ff; }
.card-green .card-num { color: #22c55e; font-size: 16px; }
.card-gold  .card-num { color: #ffd700; }
.card-blue  .card-num { color: #00b4d8; }

.two-col { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 20px; }

.panel { background: #0a1628; border: 1px solid rgba(0,212,255,0.08); border-radius: 16px; overflow: hidden; margin-bottom: 20px; }
.panel:last-child { margin-bottom: 0; }
.panel-header { display: flex; justify-content: space-between; align-items: center; padding: 18px 20px; border-bottom: 1px solid rgba(0,212,255,0.08); }
.panel-header h2 { font-size: 15px; font-weight: 600; }

/* Barras */
.barra-item { padding: 12px 20px; border-bottom: 1px solid rgba(255,255,255,0.04); }
.barra-item:last-child { border-bottom: none; }
.barra-label { display: flex; justify-content: space-between; font-size: 12px; margin-bottom: 8px; color: #f0f8ff; }
.barra-num { font-weight: 700; color: #00d4ff; }
.barra-track { height: 6px; background: rgba(255,255,255,0.06); border-radius: 4px; }
.barra-fill { height: 100%; border-radius: 4px; transition: width 1s ease; }

/* Tabla */
.tabla { width: 100%; border-collapse: collapse; }
.tabla thead tr { border-bottom: 1px solid rgba(0,212,255,0.08); }
.tabla th { padding: 13px 16px; text-align: left; font-size: 11px; font-weight: 600; color: #7a96b0; text-transform: uppercase; letter-spacing: 0.8px; }
.th-center { text-align: center !important; }
.th-right  { text-align: right !important; }
.tabla tbody tr { border-bottom: 1px solid rgba(255,255,255,0.04); transition: background 0.15s; }
.tabla tbody tr:hover { background: rgba(0,212,255,0.03); }
.tabla td { padding: 13px 16px; font-size: 13px; vertical-align: middle; }
.text-gris { color: #7a96b0; font-size: 12px; }
.curso-cell { display: flex; align-items: center; gap: 8px; }
.curso-dot { width: 8px; height: 8px; border-radius: 50%; flex-shrink: 0; }
.num-cyan   { color: #00d4ff; font-weight: 700; font-size: 15px; }
.num-yellow { color: #fbbf24; font-weight: 700; }
.num-green  { color: #22c55e; font-weight: 700; }
.ocupacion-wrap { display: flex; align-items: center; gap: 8px; justify-content: center; }
.ocup-bar { width: 60px; height: 4px; background: rgba(255,255,255,0.06); border-radius: 4px; }
.ocup-fill { height: 100%; border-radius: 4px; }
.ocupacion-wrap span { font-size: 12px; color: #7a96b0; width: 32px; }
.fila-total { border-top: 2px solid rgba(0,212,255,0.15) !important; background: rgba(0,212,255,0.04); }
.fila-total td { padding: 14px 16px; }
</style>
