<template>
  <div class="dashboard">

    <!-- Sidebar (mismo de siempre) -->
    <aside class="sidebar">
      <div class="sidebar-logo">
        <div class="logo-box">L2</div>
        <div>
          <strong>LASIN</strong>
          <span>Sistema v2.0</span>
        </div>
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

    <!-- Contenido -->
    <main class="main">

      <div class="top-bar">
        <div>
          <h1>Catálogo de Cursos</h1>
          <p>Explora y preinscríbete en los cursos disponibles del LASIN</p>
        </div>
      </div>

      <!-- Filtros -->
      <div class="filtros">
        <div class="search-wrap">
          <svg width="16" height="16" fill="none" stroke="currentColor" stroke-width="1.8" viewBox="0 0 24 24"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/></svg>
          <input v-model="busqueda" type="text" placeholder="Buscar curso..." />
        </div>
        <div class="filtro-tabs">
          <button
            v-for="cat in categorias" :key="cat"
            class="filtro-tab"
            :class="{ active: categoriaActiva === cat }"
            @click="categoriaActiva = cat"
          >{{ cat }}</button>
        </div>
      </div>

      <!-- Grid de cursos -->
      <div class="cursos-grid">
        <div
          class="curso-card"
          v-for="curso in cursosFiltrados"
          :key="curso.id"
          @click="verDetalle(curso)"
        >
          <div class="curso-header" :style="{ background: curso.color }">
            <span class="curso-emoji">{{ curso.icono }}</span>
            <span class="curso-categoria">{{ curso.categoria }}</span>
          </div>
          <div class="curso-body">
            <h3>{{ curso.nombre }}</h3>
            <p>{{ curso.descripcion }}</p>
            <div class="curso-meta">
              <span>👨‍🏫 {{ curso.docente }}</span>
              <span>📅 {{ curso.fechaInicio }}</span>
            </div>
            <div class="curso-meta">
              <span>⏱️ {{ curso.duracion }}</span>
              <span>👥 {{ curso.cupos }} cupos</span>
            </div>
            <div class="curso-footer">
              <div class="curso-precio">Bs. {{ curso.precio }}</div>
              <span class="curso-badge" :class="curso.estado">
                {{ curso.estado === 'disponible' ? 'Disponible' : curso.estado === 'proximo' ? 'Próximo' : 'Lleno' }}
              </span>
            </div>
            <button
              class="btn-preinscribir"
              :disabled="curso.estado === 'lleno'"
              @click.stop="preinscribirse(curso)"
            >
              {{ curso.estado === 'lleno' ? 'Sin cupos' : 'Preinscribirse' }}
            </button>
          </div>
        </div>
      </div>

      <!-- Sin resultados -->
      <div class="sin-resultados" v-if="cursosFiltrados.length === 0">
        <span>🔍</span>
        <p>No se encontraron cursos con ese criterio.</p>
      </div>

    </main>

    <!-- Modal de confirmación -->
    <div class="modal-overlay" v-if="modalVisible" @click="modalVisible = false">
      <div class="modal" @click.stop>
        <h2>Confirmar preinscripción</h2>
        <p>¿Deseas preinscribirte en:</p>
        <div class="modal-curso">
          <strong>{{ cursoSeleccionado?.nombre }}</strong>
          <span>Bs. {{ cursoSeleccionado?.precio }}</span>
        </div>
        <p class="modal-aviso">
          ⚠️ Recuerda que debes apersonarte al LASIN para confirmar tu pago y formalizar la inscripción.
        </p>
        <div class="modal-btns">
          <button class="btn-cancelar" @click="modalVisible = false">Cancelar</button>
          <button class="btn-confirmar" @click="confirmarPreinscripcion">Confirmar</button>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const busqueda = ref('')
const categoriaActiva = ref('Todos')
const modalVisible = ref(false)
const cursoSeleccionado = ref(null)

const categorias = ['Todos', 'Desarrollo Web', 'Data Science', 'Ciberseguridad', 'Cloud', 'IA', 'Ofimática']

const cursos = ref([
  { id: 1, nombre: 'Python para Data Science', descripcion: 'Aprende Python desde cero enfocado en análisis de datos y visualización.', docente: 'Lic. Mamani', fechaInicio: '01/03/2025', duracion: '3 meses', cupos: 8, precio: 350, categoria: 'Data Science', icono: '🐍', color: 'linear-gradient(135deg,#1d6fc4,#0ea5e9)', estado: 'disponible' },
  { id: 2, nombre: 'React & Angular Avanzado', descripcion: 'Domina los frameworks más demandados del mercado para desarrollo web moderno.', docente: 'Lic. Quispe', fechaInicio: '05/03/2025', duracion: '4 meses', cupos: 5, precio: 400, categoria: 'Desarrollo Web', icono: '⚛️', color: 'linear-gradient(135deg,#a855f7,#7c3aed)', estado: 'disponible' },
  { id: 3, nombre: 'Ethical Hacking & Pentesting', descripcion: 'Fundamentos de ciberseguridad ofensiva con laboratorios prácticos.', docente: 'Lic. Torrez', fechaInicio: '10/03/2025', duracion: '3 meses', cupos: 0, precio: 450, categoria: 'Ciberseguridad', icono: '🔐', color: 'linear-gradient(135deg,#ef4444,#b91c1c)', estado: 'lleno' },
  { id: 4, nombre: 'Azure Fundamentals', descripcion: 'Preparación para la certificación AZ-900 de Microsoft Azure.', docente: 'Lic. Condori', fechaInicio: '15/03/2025', duracion: '2 meses', cupos: 12, precio: 380, categoria: 'Cloud', icono: '☁️', color: 'linear-gradient(135deg,#0ea5e9,#0284c7)', estado: 'proximo' },
  { id: 5, nombre: 'Machine Learning Aplicado', descripcion: 'Algoritmos de ML con scikit-learn y casos reales del mercado laboral.', docente: 'Lic. Mamani', fechaInicio: '20/03/2025', duracion: '4 meses', cupos: 10, precio: 480, categoria: 'IA', icono: '🤖', color: 'linear-gradient(135deg,#f59e0b,#d97706)', estado: 'disponible' },
  { id: 6, nombre: 'Excel & Power BI Avanzado', descripcion: 'Análisis de datos empresariales y dashboards profesionales.', docente: 'Lic. Flores', fechaInicio: '01/03/2025', duracion: '2 meses', cupos: 15, precio: 250, categoria: 'Ofimática', icono: '📊', color: 'linear-gradient(135deg,#22c55e,#16a34a)', estado: 'disponible' },
  { id: 7, nombre: 'Docker & Kubernetes', descripcion: 'Contenedores y orquestación para entornos de producción modernos.', docente: 'Lic. Quispe', fechaInicio: '12/03/2025', duracion: '3 meses', cupos: 7, precio: 420, categoria: 'Desarrollo Web', icono: '🐳', color: 'linear-gradient(135deg,#06b6d4,#0891b2)', estado: 'disponible' },
  { id: 8, nombre: 'Inteligencia Artificial con Python', descripcion: 'LLMs, IA generativa y automatización con Python y Azure AI.', docente: 'Lic. Mamani', fechaInicio: '25/03/2025', duracion: '4 meses', cupos: 6, precio: 500, categoria: 'IA', icono: '✨', color: 'linear-gradient(135deg,#8b5cf6,#6d28d9)', estado: 'proximo' },
])

const cursosFiltrados = computed(() => {
  return cursos.value.filter(c => {
    const matchBusqueda = c.nombre.toLowerCase().includes(busqueda.value.toLowerCase())
    const matchCategoria = categoriaActiva.value === 'Todos' || c.categoria === categoriaActiva.value
    return matchBusqueda && matchCategoria
  })
})

function preinscribirse(curso) {
  if (curso.estado === 'lleno') return
  cursoSeleccionado.value = curso
  modalVisible.value = true
}

function confirmarPreinscripcion() {
  // Aquí irá la llamada a Flask
  alert(`✅ Preinscripción enviada para: ${cursoSeleccionado.value.nombre}\n\nRecuerda ir al LASIN a confirmar tu pago.`)
  modalVisible.value = false
}

function verDetalle(curso) {
  // Por ahora muestra el modal, luego navegará a una vista de detalle
  preinscribirse(curso)
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;500;600;700&display=swap');
* { box-sizing: border-box; margin: 0; padding: 0; }

.dashboard { font-family: 'Sora', sans-serif; display: flex; min-height: 100vh; background: #070f1f; color: #f8faff; }

/* Sidebar igual al dashboard */
.sidebar { width: 260px; flex-shrink: 0; background: rgba(255,255,255,0.03); border-right: 1px solid rgba(255,255,255,0.07); display: flex; flex-direction: column; padding: 28px 20px; }
.sidebar-logo { display: flex; align-items: center; gap: 12px; margin-bottom: 40px; padding: 0 8px; }
.logo-box { width: 40px; height: 40px; background: linear-gradient(135deg, #1d6fc4, #00d4ff); border-radius: 10px; display: flex; align-items: center; justify-content: center; font-size: 14px; font-weight: 700; color: white; flex-shrink: 0; }
.sidebar-logo strong { display: block; font-size: 15px; font-weight: 700; }
.sidebar-logo span { font-size: 11px; color: #8a9bb5; }
.sidebar-nav { display: flex; flex-direction: column; gap: 4px; flex: 1; }
.nav-item { display: flex; align-items: center; gap: 12px; padding: 11px 14px; border-radius: 10px; color: #8a9bb5; text-decoration: none; font-size: 14px; font-weight: 500; transition: all 0.2s; }
.nav-item:hover { background: rgba(255,255,255,0.05); color: white; }
.nav-item.router-link-active { background: rgba(29,111,196,0.2); color: #3b9eff; }
.sidebar-footer { border-top: 1px solid rgba(255,255,255,0.07); padding-top: 20px; }
.user-info { display: flex; align-items: center; gap: 10px; margin-bottom: 12px; }
.user-avatar { width: 36px; height: 36px; border-radius: 50%; background: linear-gradient(135deg, #1d6fc4, #a855f7); display: flex; align-items: center; justify-content: center; font-size: 12px; font-weight: 700; flex-shrink: 0; }
.user-info strong { display: block; font-size: 13px; }
.user-info span { font-size: 11px; color: #8a9bb5; }
.btn-logout { width: 100%; display: flex; align-items: center; gap: 8px; padding: 9px 14px; background: transparent; border: 1px solid rgba(255,255,255,0.08); border-radius: 8px; color: #8a9bb5; font-family: 'Sora', sans-serif; font-size: 13px; cursor: pointer; transition: all 0.2s; }
.btn-logout:hover { border-color: rgba(220,38,38,0.4); color: #fca5a5; }

/* Main */
.main { flex: 1; padding: 36px 40px; overflow-y: auto; }
.top-bar { margin-bottom: 28px; }
.top-bar h1 { font-size: 26px; font-weight: 700; margin-bottom: 4px; }
.top-bar p { font-size: 14px; color: #8a9bb5; }

/* Filtros */
.filtros { display: flex; gap: 16px; align-items: center; margin-bottom: 28px; flex-wrap: wrap; }
.search-wrap { position: relative; }
.search-wrap svg { position: absolute; left: 14px; top: 50%; transform: translateY(-50%); color: #8a9bb5; pointer-events: none; }
.search-wrap input { padding: 10px 16px 10px 42px; background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.08); border-radius: 10px; color: white; font-family: 'Sora', sans-serif; font-size: 14px; outline: none; width: 240px; }
.search-wrap input::placeholder { color: #8a9bb5; }
.search-wrap input:focus { border-color: #3b9eff; }
.filtro-tabs { display: flex; gap: 8px; flex-wrap: wrap; }
.filtro-tab { padding: 8px 16px; background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.08); border-radius: 100px; color: #8a9bb5; font-family: 'Sora', sans-serif; font-size: 12px; cursor: pointer; transition: all 0.2s; }
.filtro-tab:hover { color: white; border-color: rgba(255,255,255,0.2); }
.filtro-tab.active { background: rgba(29,111,196,0.2); border-color: rgba(29,111,196,0.4); color: #3b9eff; }

/* Grid cursos */
.cursos-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 20px; }
.curso-card { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.07); border-radius: 16px; overflow: hidden; cursor: pointer; transition: all 0.25s; }
.curso-card:hover { transform: translateY(-4px); border-color: rgba(255,255,255,0.15); box-shadow: 0 12px 40px rgba(0,0,0,0.4); }
.curso-header { padding: 24px; display: flex; justify-content: space-between; align-items: flex-start; min-height: 90px; }
.curso-emoji { font-size: 32px; }
.curso-categoria { font-size: 10px; font-weight: 600; letter-spacing: 1px; text-transform: uppercase; background: rgba(255,255,255,0.2); padding: 4px 10px; border-radius: 100px; }
.curso-body { padding: 20px; }
.curso-body h3 { font-size: 15px; font-weight: 700; margin-bottom: 8px; }
.curso-body p { font-size: 12px; color: #8a9bb5; line-height: 1.6; margin-bottom: 14px; }
.curso-meta { display: flex; gap: 16px; margin-bottom: 6px; }
.curso-meta span { font-size: 11px; color: #8a9bb5; }
.curso-footer { display: flex; justify-content: space-between; align-items: center; margin-top: 14px; margin-bottom: 14px; }
.curso-precio { font-size: 18px; font-weight: 700; color: white; }
.curso-badge { font-size: 10px; font-weight: 600; padding: 4px 10px; border-radius: 100px; }
.curso-badge.disponible { background: rgba(34,197,94,0.15); color: #22c55e; }
.curso-badge.proximo { background: rgba(251,191,36,0.15); color: #fbbf24; }
.curso-badge.lleno { background: rgba(220,38,38,0.15); color: #f87171; }
.btn-preinscribir { width: 100%; padding: 11px; background: linear-gradient(135deg, #1d6fc4, #1557a0); border: none; border-radius: 10px; color: white; font-family: 'Sora', sans-serif; font-size: 13px; font-weight: 600; cursor: pointer; transition: all 0.2s; }
.btn-preinscribir:hover:not(:disabled) { transform: translateY(-1px); box-shadow: 0 6px 20px rgba(29,111,196,0.4); }
.btn-preinscribir:disabled { opacity: 0.4; cursor: not-allowed; }

/* Sin resultados */
.sin-resultados { text-align: center; padding: 60px; color: #8a9bb5; }
.sin-resultados span { font-size: 48px; display: block; margin-bottom: 16px; }

/* Modal */
.modal-overlay { position: fixed; inset: 0; background: rgba(0,0,0,0.7); backdrop-filter: blur(4px); display: flex; align-items: center; justify-content: center; z-index: 100; }
.modal { background: #0f2447; border: 1px solid rgba(255,255,255,0.1); border-radius: 20px; padding: 32px; width: 420px; }
.modal h2 { font-size: 20px; font-weight: 700; margin-bottom: 8px; }
.modal p { font-size: 14px; color: #8a9bb5; margin-bottom: 16px; }
.modal-curso { background: rgba(255,255,255,0.05); border-radius: 12px; padding: 16px; margin-bottom: 16px; display: flex; justify-content: space-between; align-items: center; }
.modal-curso strong { font-size: 15px; }
.modal-curso span { font-size: 18px; font-weight: 700; color: #3b9eff; }
.modal-aviso { background: rgba(251,191,36,0.1); border: 1px solid rgba(251,191,36,0.2); border-radius: 10px; padding: 12px 16px; font-size: 12px; color: #fbbf24 !important; margin-bottom: 24px; }
.modal-btns { display: flex; gap: 12px; }
.btn-cancelar { flex: 1; padding: 12px; background: transparent; border: 1px solid rgba(255,255,255,0.1); border-radius: 10px; color: #8a9bb5; font-family: 'Sora', sans-serif; font-size: 14px; cursor: pointer; }
.btn-confirmar { flex: 1; padding: 12px; background: linear-gradient(135deg, #1d6fc4, #1557a0); border: none; border-radius: 10px; color: white; font-family: 'Sora', sans-serif; font-size: 14px; font-weight: 600; cursor: pointer; }
.btn-confirmar:hover { box-shadow: 0 6px 20px rgba(29,111,196,0.4); }
</style>