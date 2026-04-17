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
          <h1>Gestión de Usuarios</h1>
          <p>Crea, edita y administra todos los usuarios del sistema</p>
        </div>
        <button class="btn-nuevo" @click="abrirModalNuevo">
          + Nuevo usuario
        </button>
      </div>

      <!-- Filtros -->
      <div class="filtros">
        <div class="search-wrap">
          <svg width="15" height="15" fill="none" stroke="currentColor" stroke-width="1.8" viewBox="0 0 24 24"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/></svg>
          <input v-model="busqueda" type="text" placeholder="Buscar usuario..."/>
        </div>
        <div class="filtro-tabs">
          <button
            v-for="f in filtros" :key="f.value"
            class="filtro-tab"
            :class="{ active: filtroRol === f.value }"
            @click="filtroRol = f.value"
          >
            {{ f.label }}
            <span class="filtro-count">{{ contarPorRol(f.value) }}</span>
          </button>
        </div>
      </div>

      <!-- Tabla -->
      <div class="panel">
        <table class="tabla">
          <thead>
            <tr>
              <th>Usuario</th>
              <th>Correo</th>
              <th>Rol</th>
              <th>Estado</th>
              <th>Fecha registro</th>
              <th class="th-center">Acciones</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="u in usuariosFiltrados" :key="u.id">
              <td>
                <div class="user-cell">
                  <div class="user-avatar-sm" :style="{ background: colorRol(u.rol) }">
                    {{ iniciales(u.nombre) }}
                  </div>
                  <div>
                    <strong>{{ u.nombre }}</strong>
                    <span>{{ u.carrera }}</span>
                  </div>
                </div>
              </td>
              <td class="text-gris">{{ u.email }}</td>
              <td>
                <span class="badge-rol" :class="u.rol">{{ labelRol(u.rol) }}</span>
              </td>
              <td>
                <span class="badge-estado" :class="u.activo ? 'activo' : 'inactivo'">
                  {{ u.activo ? '● Activo' : '○ Inactivo' }}
                </span>
              </td>
              <td class="text-gris">{{ u.fechaRegistro }}</td>
              <td class="th-center">
                <div class="acciones-btns">
                  <button class="btn-edit" @click="editarUsuario(u)" title="Editar">✏️</button>
                  <button
                    class="btn-toggle"
                    :class="u.activo ? 'desactivar' : 'activar'"
                    @click="toggleEstado(u)"
                    :title="u.activo ? 'Desactivar' : 'Activar'"
                  >
                    {{ u.activo ? '🔒' : '🔓' }}
                  </button>
                  <button class="btn-delete" @click="eliminarUsuario(u)" title="Eliminar">🗑️</button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
        <div class="sin-resultados" v-if="usuariosFiltrados.length === 0">
          <span>🔍</span>
          <p>No se encontraron usuarios con ese criterio.</p>
        </div>
      </div>

    </main>

    <!-- Modal crear/editar usuario -->
    <div class="modal-overlay" v-if="modalVisible" @click.self="modalVisible = false">
      <div class="modal">
        <div class="modal-header">
          <h2>{{ modoEdicion ? '✏️ Editar usuario' : '➕ Nuevo usuario' }}</h2>
          <button class="btn-cerrar-modal" @click="modalVisible = false">✕</button>
        </div>
        <div class="modal-body">
          <div class="form-grid">
            <div class="field">
              <label>Nombre completo</label>
              <input v-model="form.nombre" type="text" class="text-input" placeholder="Ej: Ana Flores"/>
            </div>
            <div class="field">
              <label>Apellido</label>
              <input v-model="form.apellido" type="text" class="text-input" placeholder="Ej: García"/>
            </div>
            <div class="field full">
              <label>Correo institucional</label>
              <input v-model="form.email" type="email" class="text-input" placeholder="usuario@umsa.bo"/>
            </div>
            <div class="field">
              <label>Rol</label>
              <select v-model="form.rol" class="select-input">
                <option value="estudiante">🎓 Estudiante</option>
                <option value="docente">👨‍🏫 Docente</option>
                <option value="admin">🗂️ Administrador</option>
                <option value="superadmin">⚙️ Super Admin</option>
              </select>
            </div>
            <div class="field">
              <label>Carrera / Área</label>
              <input v-model="form.carrera" type="text" class="text-input" placeholder="Ej: Informática"/>
            </div>
            <div class="field full" v-if="!modoEdicion">
              <label>Contraseña temporal</label>
              <input v-model="form.password" type="password" class="text-input" placeholder="••••••••"/>
            </div>
          </div>
        </div>
        <div class="modal-footer">
          <button class="btn-cancelar" @click="modalVisible = false">Cancelar</button>
          <button class="btn-guardar" @click="guardarUsuario">
            {{ modoEdicion ? '✓ Guardar cambios' : '+ Crear usuario' }}
          </button>
        </div>
      </div>
    </div>

    <!-- Toast -->
    <div class="toast" :class="{ visible: toastVisible }">{{ toastMsg }}</div>

  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const busqueda   = ref('')
const filtroRol  = ref('todos')
const modalVisible = ref(false)
const modoEdicion  = ref(false)
const toastVisible = ref(false)
const toastMsg     = ref('')

const form = ref({ nombre: '', apellido: '', email: '', rol: 'estudiante', carrera: '', password: '' })
const usuarioEditando = ref(null)

const filtros = [
  { value: 'todos',      label: 'Todos'       },
  { value: 'estudiante', label: '🎓 Estudiantes' },
  { value: 'docente',    label: '👨‍🏫 Docentes'   },
  { value: 'admin',      label: '🗂️ Admins'      },
  { value: 'superadmin', label: '⚙️ Super Admin' },
]

const usuarios = ref([
  { id: 1,  nombre: 'Carolina Chávez',  carrera: 'Informática', email: 'carolina@est.umsa.bo',   rol: 'estudiante', activo: true,  fechaRegistro: '10/01/2025' },
  { id: 2,  nombre: 'Juan Pérez',        carrera: 'Informática', email: 'juan.p@est.umsa.bo',     rol: 'estudiante', activo: true,  fechaRegistro: '12/01/2025' },
  { id: 3,  nombre: 'María López',       carrera: 'Sistemas',    email: 'maria.l@est.umsa.bo',    rol: 'estudiante', activo: false, fechaRegistro: '15/01/2025' },
  { id: 4,  nombre: 'Carlos Quispe',     carrera: 'Informática', email: 'carlos.q@est.umsa.bo',   rol: 'estudiante', activo: true,  fechaRegistro: '18/01/2025' },
  { id: 5,  nombre: 'Lic. Henry Mamani', carrera: 'Docente LASIN', email: 'mamani@fcpn.umsa.bo',  rol: 'docente',    activo: true,  fechaRegistro: '05/01/2025' },
  { id: 6,  nombre: 'Lic. Ana Quispe',   carrera: 'Docente LASIN', email: 'quispe@fcpn.umsa.bo',  rol: 'docente',    activo: true,  fechaRegistro: '05/01/2025' },
  { id: 7,  nombre: 'Lic. Rosa Flores',  carrera: 'Docente LASIN', email: 'flores@fcpn.umsa.bo',  rol: 'docente',    activo: true,  fechaRegistro: '06/01/2025' },
  { id: 8,  nombre: 'Administrador',     carrera: 'LASIN',       email: 'admin@lasin.umsa.bo',    rol: 'admin',      activo: true,  fechaRegistro: '01/01/2025' },
  { id: 9,  nombre: 'Super Admin',       carrera: 'LASIN',       email: 'superadmin@lasin.umsa.bo', rol: 'superadmin', activo: true, fechaRegistro: '01/01/2025' },
])

const usuariosFiltrados = computed(() =>
  usuarios.value.filter(u => {
    const matchBusqueda = u.nombre.toLowerCase().includes(busqueda.value.toLowerCase()) ||
                          u.email.toLowerCase().includes(busqueda.value.toLowerCase())
    const matchRol = filtroRol.value === 'todos' || u.rol === filtroRol.value
    return matchBusqueda && matchRol
  })
)

function contarPorRol(rol) {
  if (rol === 'todos') return usuarios.value.length
  return usuarios.value.filter(u => u.rol === rol).length
}

function iniciales(nombre) {
  return nombre.split(' ').map(n => n[0]).join('').slice(0, 2).toUpperCase()
}

function labelRol(rol) {
  return { estudiante: '🎓 Estudiante', docente: '👨‍🏫 Docente', admin: '🗂️ Admin', superadmin: '⚙️ Super Admin' }[rol]
}

function colorRol(rol) {
  return {
    estudiante: 'linear-gradient(135deg,#0077b6,#00d4ff)',
    docente:    'linear-gradient(135deg,#ffd700,#f59e0b)',
    admin:      'linear-gradient(135deg,#22c55e,#16a34a)',
    superadmin: 'linear-gradient(135deg,#a855f7,#7c3aed)',
  }[rol]
}

function abrirModalNuevo() {
  modoEdicion.value = false
  form.value = { nombre: '', apellido: '', email: '', rol: 'estudiante', carrera: '', password: '' }
  modalVisible.value = true
}

function editarUsuario(u) {
  modoEdicion.value = true
  usuarioEditando.value = u
  form.value = { nombre: u.nombre, apellido: '', email: u.email, rol: u.rol, carrera: u.carrera, password: '' }
  modalVisible.value = true
}

function guardarUsuario() {
  if (!form.value.nombre || !form.value.email) {
    mostrarToast('Por favor completa nombre y correo.')
    return
  }
  if (modoEdicion.value) {
    usuarioEditando.value.nombre  = form.value.nombre
    usuarioEditando.value.email   = form.value.email
    usuarioEditando.value.rol     = form.value.rol
    usuarioEditando.value.carrera = form.value.carrera
    mostrarToast('✅ Usuario actualizado correctamente.')
  } else {
    usuarios.value.push({
      id: Date.now(),
      nombre: form.value.nombre + ' ' + form.value.apellido,
      carrera: form.value.carrera,
      email: form.value.email,
      rol: form.value.rol,
      activo: true,
      fechaRegistro: new Date().toLocaleDateString('es-BO'),
    })
    mostrarToast('✅ Usuario creado correctamente.')
  }
  modalVisible.value = false
}

function toggleEstado(u) {
  u.activo = !u.activo
  mostrarToast(u.activo ? `✅ ${u.nombre} activado.` : `🔒 ${u.nombre} desactivado.`)
}

function eliminarUsuario(u) {
  if (confirm(`¿Eliminar a ${u.nombre}? Esta acción no se puede deshacer.`)) {
    usuarios.value = usuarios.value.filter(x => x.id !== u.id)
    mostrarToast('🗑️ Usuario eliminado.')
  }
}

function mostrarToast(msg) {
  toastMsg.value = msg
  toastVisible.value = true
  setTimeout(() => toastVisible.value = false, 3000)
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
.btn-nuevo { padding: 11px 22px; background: linear-gradient(135deg,#0077b6,#00b4d8); border: none; border-radius: 10px; color: white; font-family: 'Sora', sans-serif; font-size: 14px; font-weight: 600; cursor: pointer; transition: all 0.2s; }
.btn-nuevo:hover { box-shadow: 0 6px 20px rgba(0,180,216,0.4); }
.filtros { display: flex; gap: 12px; align-items: center; margin-bottom: 20px; flex-wrap: wrap; }
.search-wrap { position: relative; }
.search-wrap svg { position: absolute; left: 13px; top: 50%; transform: translateY(-50%); color: #7a96b0; pointer-events: none; }
.search-wrap input { padding: 10px 16px 10px 38px; background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.08); border-radius: 10px; color: #f0f8ff; font-family: 'Sora', sans-serif; font-size: 13px; outline: none; width: 210px; }
.search-wrap input::placeholder { color: #7a96b0; }
.search-wrap input:focus { border-color: rgba(0,212,255,0.4); }
.filtro-tabs { display: flex; gap: 6px; flex-wrap: wrap; }
.filtro-tab { display: flex; align-items: center; gap: 6px; padding: 8px 14px; background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.07); border-radius: 100px; color: #7a96b0; font-family: 'Sora', sans-serif; font-size: 12px; cursor: pointer; transition: all 0.2s; }
.filtro-tab:hover { color: #f0f8ff; border-color: rgba(0,212,255,0.2); }
.filtro-tab.active { background: rgba(0,119,182,0.2); border-color: rgba(0,212,255,0.35); color: #00d4ff; }
.filtro-count { background: rgba(255,255,255,0.08); border-radius: 100px; padding: 1px 6px; font-size: 10px; }
.panel { background: #0a1628; border: 1px solid rgba(0,212,255,0.08); border-radius: 16px; overflow: hidden; }
.tabla { width: 100%; border-collapse: collapse; }
.tabla thead tr { border-bottom: 1px solid rgba(0,212,255,0.08); }
.tabla th { padding: 13px 16px; text-align: left; font-size: 11px; font-weight: 600; color: #7a96b0; text-transform: uppercase; letter-spacing: 0.8px; }
.th-center { text-align: center !important; }
.tabla tbody tr { border-bottom: 1px solid rgba(255,255,255,0.04); transition: background 0.15s; }
.tabla tbody tr:last-child { border-bottom: none; }
.tabla tbody tr:hover { background: rgba(0,212,255,0.03); }
.tabla td { padding: 13px 16px; font-size: 13px; vertical-align: middle; }
.text-gris { color: #7a96b0; font-size: 12px; }
.user-cell { display: flex; align-items: center; gap: 10px; }
.user-avatar-sm { width: 34px; height: 34px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 11px; font-weight: 700; flex-shrink: 0; color: white; }
.user-cell strong { display: block; font-size: 13px; font-weight: 600; margin-bottom: 2px; }
.user-cell span { font-size: 11px; color: #7a96b0; }
.badge-rol { font-size: 11px; font-weight: 600; padding: 4px 10px; border-radius: 100px; }
.badge-rol.estudiante { background: rgba(0,212,255,0.12); color: #00d4ff; }
.badge-rol.docente    { background: rgba(255,215,0,0.12);  color: #ffd700; }
.badge-rol.admin      { background: rgba(34,197,94,0.12);  color: #22c55e; }
.badge-rol.superadmin { background: rgba(168,85,247,0.12); color: #a855f7; }
.badge-estado { font-size: 11px; font-weight: 600; }
.badge-estado.activo   { color: #22c55e; }
.badge-estado.inactivo { color: #7a96b0; }
.acciones-btns { display: flex; gap: 6px; justify-content: center; }
.btn-edit, .btn-toggle, .btn-delete { width: 32px; height: 32px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.08); background: transparent; font-size: 14px; cursor: pointer; transition: all 0.2s; display: flex; align-items: center; justify-content: center; }
.btn-edit:hover   { background: rgba(0,212,255,0.12); border-color: rgba(0,212,255,0.3); }
.btn-toggle:hover { background: rgba(255,215,0,0.12); border-color: rgba(255,215,0,0.3); }
.btn-delete:hover { background: rgba(239,68,68,0.12); border-color: rgba(239,68,68,0.3); }
.sin-resultados { text-align: center; padding: 48px; color: #7a96b0; }
.sin-resultados span { font-size: 36px; display: block; margin-bottom: 12px; }
.modal-overlay { position: fixed; inset: 0; background: rgba(0,0,0,0.75); backdrop-filter: blur(6px); display: flex; align-items: center; justify-content: center; z-index: 100; }
.modal { background: #0a1628; border: 1px solid rgba(0,212,255,0.15); border-radius: 20px; width: 480px; overflow: hidden; }
.modal-header { display: flex; justify-content: space-between; align-items: center; padding: 20px 24px; border-bottom: 1px solid rgba(0,212,255,0.08); }
.modal-header h2 { font-size: 16px; font-weight: 700; }
.btn-cerrar-modal { background: transparent; border: none; color: #7a96b0; font-size: 16px; cursor: pointer; }
.btn-cerrar-modal:hover { color: #f0f8ff; }
.modal-body { padding: 24px; }
.form-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
.field.full { grid-column: 1 / -1; }
.field label { display: block; font-size: 11px; font-weight: 600; color: #7a96b0; text-transform: uppercase; letter-spacing: 0.8px; margin-bottom: 8px; }
.text-input { width: 100%; padding: 11px 14px; background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.08); border-radius: 10px; color: #f0f8ff; font-family: 'Sora', sans-serif; font-size: 13px; outline: none; transition: all 0.2s; }
.text-input:focus { border-color: rgba(0,212,255,0.4); background: rgba(0,119,182,0.08); }
.text-input::placeholder { color: #7a96b0; }
.select-input { width: 100%; padding: 11px 14px; background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.08); border-radius: 10px; color: #f0f8ff; font-family: 'Sora', sans-serif; font-size: 13px; outline: none; }
.select-input option { background: #0a1628; }
.modal-footer { display: flex; gap: 12px; padding: 16px 24px; border-top: 1px solid rgba(0,212,255,0.08); }
.btn-cancelar { flex: 1; padding: 11px; background: transparent; border: 1px solid rgba(255,255,255,0.08); border-radius: 10px; color: #7a96b0; font-family: 'Sora', sans-serif; font-size: 13px; cursor: pointer; }
.btn-guardar { flex: 2; padding: 11px; background: linear-gradient(135deg,#0077b6,#00b4d8); border: none; border-radius: 10px; color: white; font-family: 'Sora', sans-serif; font-size: 13px; font-weight: 600; cursor: pointer; }
.btn-guardar:hover { box-shadow: 0 6px 20px rgba(0,180,216,0.35); }
.toast { position: fixed; bottom: 28px; right: 28px; background: #0a1628; border: 1px solid rgba(0,212,255,0.3); color: #00d4ff; padding: 14px 22px; border-radius: 12px; font-size: 13px; font-weight: 500; transform: translateY(80px); opacity: 0; transition: all 0.3s; z-index: 200; box-shadow: 0 8px 30px rgba(0,0,0,0.4); }
.toast.visible { transform: translateY(0); opacity: 1; }
</style>