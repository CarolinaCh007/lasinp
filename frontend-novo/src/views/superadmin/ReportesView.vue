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
          <h1>Reportes Institucionales</h1>
          <p>Analítica completa del LASIN — Ciclo académico 2025</p>
        </div>
        <div class="top-actions">
          <select v-model="periodoActivo" class="select-periodo">
            <option value="2025-1">Ciclo 2025 — I</option>
            <option value="2024-2">Ciclo 2024 — II</option>
            <option value="2024-1">Ciclo 2024 — I</option>
          </select>
          <button class="btn-exportar">📄 Exportar PDF</button>
          <button class="btn-exportar excel">📊 Exportar Excel</button>
        </div>
      </div>

      <!-- KPIs globales -->
      <div class="kpis-grid">
        <div class="kpi" v-for="k in kpis" :key="k.label">
          <div class="kpi-icon" :style="{ background: k.bg }">{{ k.icono }}</div>
          <div class="kpi-data">
            <span class="kpi-num" :style="{ color: k.color }">{{ k.valor }}</span>
            <span class="kpi-label">{{ k.label }}</span>
          </div>
          <div class="kpi-trend" :class="k.trend >= 0 ? 'up' : 'down'">
            {{ k.trend >= 0 ? '↑' : '↓' }} {{ Math.abs(k.trend) }}%
          </div>
        </div>
      </div>

      <!-- Tabs de secciones -->
      <div class="tabs">
        <button
          v-for="tab in tabs" :key="tab.value"
          class="tab"
          :class="{ active: tabActivo === tab.value }"
          @click="tabActivo = tab.value"
        >{{ tab.label }}</button>
      </div>

      <!-- TAB: Inscripciones -->
      <div v-if="tabActivo === 'inscripciones'">
        <div class="two-col">
          <div class="panel">
            <div class="panel-header"><h2>📊 Inscritos por curso</h2></div>
            <div class="barra-item" v-for="c in cursos" :key="c.id">
              <div class="barra-label">
                <span>{{ c.nombre }}</span>
                <span class="barra-num" :style="{ color: c.color }">{{ c.inscritos }} / {{ c.cupoMax }}</span>
              </div>
              <div class="barra-track">
                <div class="barra-fill" :style="{ width: (c.inscritos / c.cupoMax * 100) + '%', background: c.color }"></div>
              </div>
              <div class="barra-pct">{{ Math.round(c.inscritos / c.cupoMax * 100) }}%</div>
            </div>
          </div>

          <div class="panel">
            <div class="panel-header"><h2>📈 Inscritos por mes</h2></div>
            <div class="linea-chart">
              <div class="linea-item" v-for="m in meses" :key="m.mes">
                <div class="linea-bar-wrap">
                  <div class="linea-bar" :style="{ height: (m.inscritos / maxMes * 140) + 'px', background: 'linear-gradient(180deg,#00d4ff,#0077b6)' }"></div>
                </div>
                <span class="linea-val">{{ m.inscritos }}</span>
                <span class="linea-mes">{{ m.mes }}</span>
              </div>
            </div>
          </div>
        </div>

        <div class="panel">
          <div class="panel-header"><h2>📋 Detalle completo por curso</h2></div>
          <table class="tabla">
            <thead>
              <tr>
                <th>Curso</th>
                <th>Docente</th>
                <th class="th-center">Inscritos</th>
                <th class="th-center">Pendientes</th>
                <th class="th-center">Ocupación</th>
                <th class="th-center">Promedio</th>
                <th class="th-right">Ingresos</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="c in cursos" :key="c.id">
                <td>
                  <div class="curso-cell">
                    <div class="cdot" :style="{ background: c.color }"></div>
                    <strong>{{ c.nombre }}</strong>
                  </div>
                </td>
                <td class="text-gris">{{ c.docente }}</td>
                <td class="th-center"><span class="num-cyan">{{ c.inscritos }}</span></td>
                <td class="th-center"><span class="num-yellow">{{ c.pendientes }}</span></td>
                <td class="th-center">
                  <div class="ocup-wrap">
                    <div class="ocup-bar"><div class="ocup-fill" :style="{ width: (c.inscritos/c.cupoMax*100)+'%', background: c.color }"></div></div>
                    <span>{{ Math.round(c.inscritos/c.cupoMax*100) }}%</span>
                  </div>
                </td>
                <td class="th-center"><span :class="notaClase(c.promedio)">{{ c.promedio }}</span></td>
                <td class="th-right"><strong>Bs. {{ (c.inscritos * c.precio).toLocaleString() }}</strong></td>
              </tr>
            </tbody>
            <tfoot>
              <tr class="fila-total">
                <td colspan="2"><strong>TOTAL</strong></td>
                <td class="th-center"><strong class="num-cyan">{{ totalInscritos }}</strong></td>
                <td class="th-center"><strong class="num-yellow">{{ totalPendientes }}</strong></td>
                <td class="th-center">—</td>
                <td class="th-center"><strong style="color:#00d4ff">{{ promedioGeneral }}</strong></td>
                <td class="th-right"><strong>Bs. {{ totalIngresos.toLocaleString() }}</strong></td>
              </tr>
            </tfoot>
          </table>
        </div>
      </div>

      <!-- TAB: Financiero -->
      <div v-if="tabActivo === 'financiero'">
        <div class="cards-fin">
          <div class="card-fin" v-for="f in finanzas" :key="f.label">
            <span class="fin-icon">{{ f.icono }}</span>
            <span class="fin-num" :style="{ color: f.color }">{{ f.valor }}</span>
            <span class="fin-label">{{ f.label }}</span>
          </div>
        </div>
        <div class="panel">
          <div class="panel-header"><h2>💰 Ingresos por curso</h2></div>
          <div class="barra-item" v-for="c in cursosOrdenadosPorIngreso" :key="c.id">
            <div class="barra-label">
              <span>{{ c.nombre }}</span>
              <span class="barra-num" style="color:#22c55e">Bs. {{ (c.inscritos * c.precio).toLocaleString() }}</span>
            </div>
            <div class="barra-track">
              <div class="barra-fill" :style="{ width: (c.inscritos * c.precio / maxIngreso * 100) + '%', background: 'linear-gradient(90deg,#22c55e,#16a34a)' }"></div>
            </div>
            <div class="barra-pct" style="color:#22c55e">{{ Math.round(c.inscritos * c.precio / totalIngresos * 100) }}%</div>
          </div>
        </div>
      </div>

      <!-- TAB: Académico -->
      <div v-if="tabActivo === 'academico'">
        <div class="two-col">
          <div class="panel">
            <div class="panel-header"><h2>🎓 Rendimiento por curso</h2></div>
            <div class="rend-item" v-for="c in cursos" :key="c.id">
              <div class="rend-info">
                <strong>{{ c.nombre }}</strong>
                <span>{{ c.docente }}</span>
              </div>
              <div class="rend-bars">
                <div class="rend-row">
                  <span class="rend-label-sm">Promedio</span>
                  <div class="rend-track">
                    <div class="rend-fill" :style="{ width: c.promedio + '%', background: c.color }"></div>
                  </div>
                  <span :class="notaClase(c.promedio)">{{ c.promedio }}</span>
                </div>
                <div class="rend-row">
                  <span class="rend-label-sm">Asistencia</span>
                  <div class="rend-track">
                    <div class="rend-fill" :style="{ width: c.asistencia + '%', background: '#22c55e' }"></div>
                  </div>
                  <span class="num-green">{{ c.asistencia }}%</span>
                </div>
              </div>
            </div>
          </div>

          <div class="panel">
            <div class="panel-header"><h2>📊 Distribución de notas</h2></div>
            <div class="dist-item" v-for="d in distribucion" :key="d.rango">
              <div class="dist-info">
                <span class="dist-rango" :style="{ color: d.color }">{{ d.rango }}</span>
                <span class="dist-label">{{ d.label }}</span>
              </div>
              <div class="dist-track">
                <div class="dist-fill" :style="{ width: d.pct + '%', background: d.color }"></div>
              </div>
              <span class="dist-pct" :style="{ color: d.color }">{{ d.pct }}%</span>
            </div>

            <div class="resumen-aprobacion">
              <div class="apr-item">
                <span class="apr-num" style="color:#22c55e">82%</span>
                <span class="apr-label">Tasa de aprobación</span>
              </div>
              <div class="apr-div"></div>
              <div class="apr-item">
                <span class="apr-num" style="color:#ef4444">18%</span>
                <span class="apr-label">Tasa de reprobación</span>
              </div>
              <div class="apr-div"></div>
              <div class="apr-item">
                <span class="apr-num" style="color:#00d4ff">81</span>
                <span class="apr-label">Promedio global</span>
              </div>
            </div>
          </div>
        </div>
      </div>

    </main>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const periodoActivo = ref('2025-1')
const tabActivo     = ref('inscripciones')

const tabs = [
  { value: 'inscripciones', label: '👥 Inscripciones' },
  { value: 'financiero',    label: '💰 Financiero'    },
  { value: 'academico',     label: '🎓 Académico'     },
]

const kpis = ref([
  { icono: '👥', label: 'Total inscritos',    valor: '99',          color: '#00d4ff', bg: 'rgba(0,212,255,0.12)',  trend: 15  },
  { icono: '💰', label: 'Ingresos del ciclo', valor: 'Bs. 34,200',  color: '#22c55e', bg: 'rgba(34,197,94,0.12)', trend: 8   },
  { icono: '📊', label: 'Promedio general',   valor: '81',          color: '#ffd700', bg: 'rgba(255,215,0,0.12)', trend: 4   },
  { icono: '✅', label: 'Tasa aprobación',    valor: '82%',         color: '#a855f7', bg: 'rgba(168,85,247,0.12)',trend: 3   },
  { icono: '📅', label: 'Asistencia media',   valor: '88%',         color: '#00b4d8', bg: 'rgba(0,180,216,0.12)', trend: -1  },
])

const cursos = ref([
  { id: 1, nombre: 'Python Data Science',  docente: 'Lic. Mamani', inscritos: 28, pendientes: 3, cupoMax: 30, promedio: 84, asistencia: 91, precio: 350, color: '#00d4ff' },
  { id: 2, nombre: 'React & Angular',       docente: 'Lic. Quispe',  inscritos: 22, pendientes: 2, cupoMax: 25, promedio: 79, asistencia: 87, precio: 400, color: '#a855f7' },
  { id: 3, nombre: 'Azure Fundamentals',    docente: 'Lic. Condori', inscritos: 15, pendientes: 4, cupoMax: 20, promedio: 76, asistencia: 85, precio: 380, color: '#0077b6' },
  { id: 4, nombre: 'Machine Learning',      docente: 'Lic. Mamani', inscritos: 18, pendientes: 2, cupoMax: 20, promedio: 88, asistencia: 93, precio: 480, color: '#ffd700' },
  { id: 5, nombre: 'Excel & Power BI',      docente: 'Lic. Flores',  inscritos: 16, pendientes: 1, cupoMax: 20, promedio: 81, asistencia: 89, precio: 250, color: '#22c55e' },
])

const meses = ref([
  { mes: 'Oct', inscritos: 12 },
  { mes: 'Nov', inscritos: 18 },
  { mes: 'Dic', inscritos: 8  },
  { mes: 'Ene', inscritos: 25 },
  { mes: 'Feb', inscritos: 36 },
])

const distribucion = ref([
  { rango: '91–100', label: 'Excelente', pct: 22, color: '#00d4ff' },
  { rango: '76–90',  label: 'Bueno',     pct: 38, color: '#22c55e' },
  { rango: '61–75',  label: 'Regular',   pct: 22, color: '#ffd700' },
  { rango: '51–60',  label: 'Suficiente',pct: 10, color: '#f59e0b' },
  { rango: '0–50',   label: 'Reprobado', pct: 8,  color: '#ef4444' },
])

const finanzas = ref([
  { icono: '💰', label: 'Ingresos totales',      valor: 'Bs. 34,200', color: '#22c55e' },
  { icono: '⏳', label: 'Pendientes de cobro',   valor: 'Bs. 4,200',  color: '#fbbf24' },
  { icono: '📈', label: 'Ingreso promedio/curso', valor: 'Bs. 6,840',  color: '#00d4ff' },
  { icono: '🏆', label: 'Curso más rentable',     valor: 'Machine ML', color: '#a855f7' },
])

const maxMes     = computed(() => Math.max(...meses.value.map(m => m.inscritos)))
const maxIngreso = computed(() => Math.max(...cursos.value.map(c => c.inscritos * c.precio)))

const totalInscritos  = computed(() => cursos.value.reduce((s, c) => s + c.inscritos, 0))
const totalPendientes = computed(() => cursos.value.reduce((s, c) => s + c.pendientes, 0))
const totalIngresos   = computed(() => cursos.value.reduce((s, c) => s + c.inscritos * c.precio, 0))
const promedioGeneral = computed(() => Math.round(cursos.value.reduce((s, c) => s + c.promedio, 0) / cursos.value.length))

const cursosOrdenadosPorIngreso = computed(() =>
  [...cursos.value].sort((a, b) => (b.inscritos * b.precio) - (a.inscritos * a.precio))
)

function notaClase(nota) {
  if (nota >= 80) return 'num-cyan'
  if (nota >= 60) return 'num-yellow'
  return 'num-red'
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
.top-bar { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 24px; }
.top-bar h1 { font-size: 26px; font-weight: 700; margin-bottom: 4px; }
.top-bar p { font-size: 14px; color: #7a96b0; }
.top-actions { display: flex; gap: 10px; align-items: center; }
.select-periodo { padding: 9px 14px; background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.08); border-radius: 10px; color: #f0f8ff; font-family: 'Sora', sans-serif; font-size: 13px; outline: none; }
.select-periodo option { background: #0a1628; }
.btn-exportar { padding: 9px 18px; background: rgba(255,215,0,0.1); border: 1px solid rgba(255,215,0,0.25); border-radius: 10px; color: #ffd700; font-family: 'Sora', sans-serif; font-size: 12px; font-weight: 600; cursor: pointer; transition: all 0.2s; white-space: nowrap; }
.btn-exportar:hover { background: rgba(255,215,0,0.18); }
.btn-exportar.excel { background: rgba(34,197,94,0.1); border-color: rgba(34,197,94,0.25); color: #22c55e; }
.btn-exportar.excel:hover { background: rgba(34,197,94,0.18); }
.kpis-grid { display: grid; grid-template-columns: repeat(5,1fr); gap: 14px; margin-bottom: 24px; }
.kpi { background: #0a1628; border: 1px solid rgba(0,212,255,0.08); border-radius: 16px; padding: 18px; display: flex; align-items: center; gap: 12px; }
.kpi-icon { width: 44px; height: 44px; border-radius: 12px; display: flex; align-items: center; justify-content: center; font-size: 20px; flex-shrink: 0; }
.kpi-data { flex: 1; }
.kpi-num { display: block; font-size: 20px; font-weight: 800; line-height: 1; margin-bottom: 4px; }
.kpi-label { font-size: 10px; color: #7a96b0; text-transform: uppercase; letter-spacing: 0.5px; }
.kpi-trend { font-size: 11px; font-weight: 700; padding: 3px 8px; border-radius: 100px; white-space: nowrap; }
.kpi-trend.up   { background: rgba(34,197,94,0.12); color: #22c55e; }
.kpi-trend.down { background: rgba(239,68,68,0.12); color: #ef4444; }
.tabs { display: flex; gap: 8px; margin-bottom: 20px; }
.tab { padding: 10px 22px; background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.07); border-radius: 100px; color: #7a96b0; font-family: 'Sora', sans-serif; font-size: 13px; cursor: pointer; transition: all 0.2s; }
.tab:hover { color: #f0f8ff; border-color: rgba(0,212,255,0.2); }
.tab.active { background: rgba(0,119,182,0.2); border-color: rgba(0,212,255,0.35); color: #00d4ff; }
.two-col { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 20px; }
.panel { background: #0a1628; border: 1px solid rgba(0,212,255,0.08); border-radius: 16px; overflow: hidden; margin-bottom: 20px; }
.panel:last-child { margin-bottom: 0; }
.panel-header { display: flex; justify-content: space-between; align-items: center; padding: 18px 20px; border-bottom: 1px solid rgba(0,212,255,0.08); }
.panel-header h2 { font-size: 15px; font-weight: 600; }
.barra-item { display: flex; align-items: center; gap: 12px; padding: 12px 20px; border-bottom: 1px solid rgba(255,255,255,0.04); }
.barra-item:last-child { border-bottom: none; }
.barra-label { display: flex; flex-direction: column; gap: 2px; width: 180px; flex-shrink: 0; }
.barra-label span:first-child { font-size: 12px; font-weight: 600; }
.barra-num { font-size: 11px; font-weight: 700; }
.barra-track { flex: 1; height: 6px; background: rgba(255,255,255,0.06); border-radius: 4px; }
.barra-fill { height: 100%; border-radius: 4px; transition: width 1s ease; }
.barra-pct { font-size: 11px; color: #7a96b0; width: 32px; text-align: right; }
.linea-chart { display: flex; align-items: flex-end; gap: 12px; padding: 20px; height: 200px; }
.linea-item { flex: 1; display: flex; flex-direction: column; align-items: center; gap: 6px; height: 100%; justify-content: flex-end; }
.linea-bar-wrap { flex: 1; display: flex; align-items: flex-end; width: 100%; }
.linea-bar { width: 100%; border-radius: 6px 6px 0 0; transition: height 1s ease; min-height: 4px; }
.linea-val { font-size: 12px; font-weight: 700; color: #00d4ff; }
.linea-mes { font-size: 11px; color: #7a96b0; }
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
.cdot { width: 8px; height: 8px; border-radius: 50%; flex-shrink: 0; }
.num-cyan   { color: #00d4ff; font-weight: 700; }
.num-yellow { color: #fbbf24; font-weight: 700; }
.num-green  { color: #22c55e; font-weight: 700; }
.num-red    { color: #ef4444; font-weight: 700; }
.ocup-wrap { display: flex; align-items: center; gap: 6px; justify-content: center; }
.ocup-bar { width: 50px; height: 4px; background: rgba(255,255,255,0.06); border-radius: 4px; }
.ocup-fill { height: 100%; border-radius: 4px; }
.ocup-wrap span { font-size: 11px; color: #7a96b0; }
.fila-total { border-top: 2px solid rgba(0,212,255,0.15) !important; background: rgba(0,212,255,0.04); }
.fila-total td { padding: 14px 16px; }
.cards-fin { display: grid; grid-template-columns: repeat(4,1fr); gap: 16px; margin-bottom: 20px; }
.card-fin { background: #0a1628; border: 1px solid rgba(0,212,255,0.08); border-radius: 16px; padding: 22px; display: flex; flex-direction: column; align-items: center; gap: 6px; text-align: center; }
.fin-icon { font-size: 26px; }
.fin-num { font-size: 20px; font-weight: 800; }
.fin-label { font-size: 11px; color: #7a96b0; text-transform: uppercase; letter-spacing: 0.5px; }
.rend-item { display: flex; align-items: flex-start; gap: 14px; padding: 14px 20px; border-bottom: 1px solid rgba(255,255,255,0.04); }
.rend-item:last-child { border-bottom: none; }
.rend-info { width: 140px; flex-shrink: 0; }
.rend-info strong { display: block; font-size: 12px; font-weight: 600; margin-bottom: 3px; }
.rend-info span { font-size: 11px; color: #7a96b0; }
.rend-bars { flex: 1; display: flex; flex-direction: column; gap: 8px; }
.rend-row { display: flex; align-items: center; gap: 8px; }
.rend-label-sm { font-size: 10px; color: #7a96b0; width: 58px; flex-shrink: 0; }
.rend-track { flex: 1; height: 5px; background: rgba(255,255,255,0.06); border-radius: 4px; }
.rend-fill { height: 100%; border-radius: 4px; }
.rend-row span:last-child { font-size: 11px; font-weight: 700; width: 36px; text-align: right; }
.dist-item { display: flex; align-items: center; gap: 12px; padding: 12px 20px; border-bottom: 1px solid rgba(255,255,255,0.04); }
.dist-item:last-child { border-bottom: none; }
.dist-info { width: 110px; flex-shrink: 0; }
.dist-rango { display: block; font-size: 13px; font-weight: 700; }
.dist-label { font-size: 11px; color: #7a96b0; }
.dist-track { flex: 1; height: 6px; background: rgba(255,255,255,0.06); border-radius: 4px; }
.dist-fill { height: 100%; border-radius: 4px; transition: width 1s ease; }
.dist-pct { font-size: 12px; font-weight: 700; width: 36px; text-align: right; }
.resumen-aprobacion { display: flex; justify-content: center; gap: 0; border-top: 1px solid rgba(0,212,255,0.08); margin-top: 4px; }
.apr-item { flex: 1; text-align: center; padding: 16px 8px; }
.apr-num { display: block; font-size: 24px; font-weight: 800; margin-bottom: 4px; }
.apr-label { font-size: 10px; color: #7a96b0; text-transform: uppercase; letter-spacing: 0.5px; }
.apr-div { width: 1px; background: rgba(0,212,255,0.08); align-self: center; height: 36px; }
</style>