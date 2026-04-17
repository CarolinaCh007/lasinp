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
          <h1>Mi Perfil</h1>
          <p>Gestiona tu información personal y académica</p>
        </div>
        <button class="btn-guardar" v-if="editando" @click="guardarCambios">
          ✓ Guardar cambios
        </button>
        <button class="btn-editar" v-else @click="editando = true">
          ✏️ Editar perfil
        </button>
      </div>

      <div class="perfil-grid">

        <!-- Card principal -->
        <div class="card-perfil">
          <div class="perfil-banner"></div>
          <div class="perfil-avatar-wrap">
            <div class="perfil-avatar">CA</div>
            <div class="perfil-badge">Estudiante</div>
          </div>
          <div class="perfil-nombre">
            <h2>Carolina Chávez</h2>
            <p>Carrera de Informática · UMSA</p>
          </div>

          <div class="perfil-stats">
            <div class="pstat">
              <span class="pstat-num">5</span>
              <span class="pstat-label">Completados</span>
            </div>
            <div class="pstat-div"></div>
            <div class="pstat">
              <span class="pstat-num">2</span>
              <span class="pstat-label">En curso</span>
            </div>
            <div class="pstat-div"></div>
            <div class="pstat">
              <span class="pstat-num">87%</span>
              <span class="pstat-label">Promedio</span>
            </div>
          </div>

          <!-- Rutas de aprendizaje -->
          <div class="rutas-section">
            <p class="rutas-title">Ruta en progreso</p>
            <div class="ruta-item" v-for="ruta in rutas" :key="ruta.nombre">
              <div class="ruta-info">
                <span>{{ ruta.icono }} {{ ruta.nombre }}</span>
                <span class="ruta-pct">{{ ruta.pct }}%</span>
              </div>
              <div class="ruta-bar">
                <div class="ruta-fill" :style="{ width: ruta.pct + '%', background: ruta.color }"></div>
              </div>
            </div>
          </div>
        </div>

        <!-- Formulario de datos -->
        <div class="card-datos">
          <h3>Información personal</h3>

          <div class="form-grid">
            <div class="field">
              <label>Nombre completo</label>
              <input v-model="perfil.nombre" :disabled="!editando" type="text"/>
            </div>
            <div class="field">
              <label>Apellido</label>
              <input v-model="perfil.apellido" :disabled="!editando" type="text"/>
            </div>
            <div class="field">
              <label>Correo institucional</label>
              <input v-model="perfil.email" :disabled="!editando" type="email"/>
            </div>
            <div class="field">
              <label>Teléfono</label>
              <input v-model="perfil.telefono" :disabled="!editando" type="tel"/>
            </div>
            <div class="field full">
              <label>Dirección</label>
              <input v-model="perfil.direccion" :disabled="!editando" type="text"/>
            </div>
            <div class="field">
              <label>Semestre actual</label>
              <input v-model="perfil.semestre" :disabled="!editando" type="text"/>
            </div>
            <div class="field">
              <label>Año de ingreso</label>
              <input v-model="perfil.anioIngreso" :disabled="!editando" type="text"/>
            </div>
          </div>

          <!-- Cambiar contraseña -->
          <div class="password-section" v-if="editando">
            <h3>Cambiar contraseña</h3>
            <div class="form-grid">
              <div class="field">
                <label>Contraseña actual</label>
                <input type="password" placeholder="••••••••"/>
              </div>
              <div class="field">
                <label>Nueva contraseña</label>
                <input type="password" placeholder="••••••••"/>
              </div>
            </div>
          </div>

          <!-- Mensaje éxito -->
          <div class="success-msg" v-if="guardado">
            ✅ Perfil actualizado correctamente.
          </div>
        </div>

      </div>
    </main>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const editando = ref(false)
const guardado = ref(false)

const perfil = ref({
  nombre:      'Carolina',
  apellido:    'Chávez',
  email:       'carolina.chavez@est.umsa.bo',
  telefono:    '+591 77712345',
  direccion:   'Av. Villazon, La Paz - Bolivia',
  semestre:    '6to Semestre',
  anioIngreso: '2021',
})

const rutas = ref([
  { nombre: 'Data Science & ML', icono: '🤖', pct: 65, color: 'linear-gradient(90deg,#0077b6,#00d4ff)' },
  { nombre: 'Desarrollo Web Full Stack', icono: '💻', pct: 40, color: 'linear-gradient(90deg,#7c3aed,#a855f7)' },
])

function guardarCambios() {
  // Aquí irá la llamada a Flask
  editando.value = false
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
.user-avatar { width: 36px; height: 36px; border-radius: 50%; background: linear-gradient(135deg, #0077b6, #a855f7); display: flex; align-items: center; justify-content: center; font-size: 12px; font-weight: 700; flex-shrink: 0; }
.user-info strong { display: block; font-size: 13px; }
.user-info span { font-size: 11px; color: #7a96b0; }
.btn-logout { width: 100%; display: flex; align-items: center; gap: 8px; padding: 9px 14px; background: transparent; border: 1px solid rgba(255,255,255,0.07); border-radius: 8px; color: #7a96b0; font-family: 'Sora', sans-serif; font-size: 13px; cursor: pointer; transition: all 0.2s; }
.btn-logout:hover { border-color: rgba(239,68,68,0.4); color: #fca5a5; }

/* Main */
.main { flex: 1; padding: 36px 40px; overflow-y: auto; }
.top-bar { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 32px; }
.top-bar h1 { font-size: 26px; font-weight: 700; margin-bottom: 4px; }
.top-bar p { font-size: 14px; color: #7a96b0; }

.btn-editar { padding: 10px 22px; background: rgba(0,212,255,0.08); border: 1px solid rgba(0,212,255,0.25); border-radius: 10px; color: #00d4ff; font-family: 'Sora', sans-serif; font-size: 13px; font-weight: 600; cursor: pointer; transition: all 0.2s; }
.btn-editar:hover { background: rgba(0,212,255,0.15); }
.btn-guardar { padding: 10px 22px; background: linear-gradient(135deg, #0077b6, #00b4d8); border: none; border-radius: 10px; color: white; font-family: 'Sora', sans-serif; font-size: 13px; font-weight: 600; cursor: pointer; transition: all 0.2s; }
.btn-guardar:hover { box-shadow: 0 6px 20px rgba(0,180,216,0.35); }

/* Grid */
.perfil-grid { display: grid; grid-template-columns: 320px 1fr; gap: 24px; }

/* Card perfil */
.card-perfil { background: #0a1628; border: 1px solid rgba(0,212,255,0.08); border-radius: 20px; overflow: hidden; }
.perfil-banner { height: 90px; background: linear-gradient(135deg, #0077b6, #00d4ff, #ffd700); opacity: 0.8; }
.perfil-avatar-wrap { display: flex; justify-content: center; margin-top: -36px; margin-bottom: 12px; position: relative; }
.perfil-avatar { width: 72px; height: 72px; border-radius: 50%; background: linear-gradient(135deg, #0077b6, #a855f7); display: flex; align-items: center; justify-content: center; font-size: 22px; font-weight: 700; border: 3px solid #0a1628; }
.perfil-badge { position: absolute; bottom: 0; right: calc(50% - 60px); background: rgba(0,212,255,0.15); border: 1px solid rgba(0,212,255,0.3); border-radius: 100px; padding: 2px 10px; font-size: 10px; color: #00d4ff; font-weight: 600; }
.perfil-nombre { text-align: center; padding: 0 24px 20px; }
.perfil-nombre h2 { font-size: 18px; font-weight: 700; margin-bottom: 4px; }
.perfil-nombre p { font-size: 12px; color: #7a96b0; }

.perfil-stats { display: flex; justify-content: center; gap: 0; border-top: 1px solid rgba(0,212,255,0.08); border-bottom: 1px solid rgba(0,212,255,0.08); margin: 0 0 24px; }
.pstat { flex: 1; text-align: center; padding: 16px 8px; }
.pstat-num { display: block; font-size: 22px; font-weight: 700; color: #00d4ff; }
.pstat-label { font-size: 10px; color: #7a96b0; text-transform: uppercase; letter-spacing: 0.5px; }
.pstat-div { width: 1px; background: rgba(0,212,255,0.08); align-self: center; height: 32px; }

.rutas-section { padding: 0 24px 24px; }
.rutas-title { font-size: 11px; font-weight: 600; text-transform: uppercase; letter-spacing: 1px; color: #7a96b0; margin-bottom: 14px; }
.ruta-item { margin-bottom: 14px; }
.ruta-info { display: flex; justify-content: space-between; font-size: 12px; margin-bottom: 6px; }
.ruta-pct { color: #00d4ff; font-weight: 600; }
.ruta-bar { height: 5px; background: rgba(255,255,255,0.06); border-radius: 4px; }
.ruta-fill { height: 100%; border-radius: 4px; transition: width 1s ease; }

/* Card datos */
.card-datos { background: #0a1628; border: 1px solid rgba(0,212,255,0.08); border-radius: 20px; padding: 28px; }
.card-datos h3 { font-size: 15px; font-weight: 700; margin-bottom: 22px; color: #f0f8ff; }

.form-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 28px; }
.field.full { grid-column: 1 / -1; }

.field label { display: block; font-size: 11px; font-weight: 600; color: #7a96b0; text-transform: uppercase; letter-spacing: 0.8px; margin-bottom: 8px; }
.field input { width: 100%; padding: 12px 16px; background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.07); border-radius: 10px; color: #f0f8ff; font-family: 'Sora', sans-serif; font-size: 14px; outline: none; transition: all 0.2s; }
.field input:disabled { opacity: 0.5; cursor: not-allowed; }
.field input:focus { border-color: rgba(0,212,255,0.4); background: rgba(0,119,182,0.08); box-shadow: 0 0 0 3px rgba(0,212,255,0.07); }

.password-section { border-top: 1px solid rgba(0,212,255,0.08); padding-top: 24px; }
.password-section h3 { font-size: 15px; font-weight: 700; margin-bottom: 18px; }

.success-msg { margin-top: 20px; background: rgba(34,197,94,0.1); border: 1px solid rgba(34,197,94,0.25); color: #86efac; border-radius: 10px; padding: 12px 16px; font-size: 13px; }
</style>