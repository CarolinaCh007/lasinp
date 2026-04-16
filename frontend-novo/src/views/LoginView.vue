<template>
  <div class="login-page">

    <!-- Panel izquierdo — Hero -->
    <div class="login-hero">
      <div class="hero-content">
        <div class="hero-logo">
          <div class="sidebar-logo__box">
            <svg width="28" height="28" fill="none" stroke="currentColor" stroke-width="1.8" viewBox="0 0 24 24">
              <path d="M12 2L2 7l10 5 10-5-10-5z"/>
              <path d="M2 17l10 5 10-5"/>
              <path d="M2 12l10 5 10-5"/>
            </svg>
          </div>
          <div>
            <strong class="hero-logo__title">LASIN 2.0</strong>
            <span class="hero-logo__sub">Laboratorio Superior de Informática</span>
          </div>
        </div>

        <h1 class="hero-title">
          Gestión académica <br/>
          <span class="text-cyan">inteligente</span>
        </h1>
        <p class="hero-desc">
          Plataforma oficial del LASIN — UMSA. Administra cursos,
          estudiantes y docentes desde un solo lugar.
        </p>

        <div class="hero-stats">
          <div class="hero-stat">
            <span class="hero-stat__num text-cyan">9+</span>
            <span class="hero-stat__label">Rutas de aprendizaje</span>
          </div>
          <div class="hero-stat">
            <span class="hero-stat__num text-gold">4k+</span>
            <span class="hero-stat__label">Estudiantes formados</span>
          </div>
          <div class="hero-stat">
            <span class="hero-stat__num text-success">24/7</span>
            <span class="hero-stat__label">Disponibilidad</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Panel derecho — Formulario -->
    <div class="login-form-wrap">
      <div class="login-form">

        <div class="form-head">
          <h2>Iniciar sesión</h2>
          <p class="text-muted">Selecciona tu rol y accede al sistema</p>
        </div>

        <!-- Selector de rol -->
        <div class="role-grid">
          <button
            v-for="r in roles"
            :key="r.value"
            class="role-btn"
            :class="{ active: rolSeleccionado === r.value }"
            @click="rolSeleccionado = r.value"
          >
            <span class="role-btn__icon">{{ r.icono }}</span>
            <span class="role-btn__label">{{ r.label }}</span>
          </button>
        </div>

        <!-- Campos -->
        <div class="form-field mt-4">
          <label class="field-label">Correo institucional</label>
          <div class="search-wrap">
            <svg width="15" height="15" fill="none" stroke="currentColor" stroke-width="1.8" viewBox="0 0 24 24">
              <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/>
              <polyline points="22,6 12,13 2,6"/>
            </svg>
            <input
              v-model="email"
              type="email"
              class="input-base"
              :placeholder="placeholderEmail"
            />
          </div>
        </div>

        <div class="form-field mt-3">
          <label class="field-label">Contraseña</label>
          <div class="search-wrap">
            <svg width="15" height="15" fill="none" stroke="currentColor" stroke-width="1.8" viewBox="0 0 24 24">
              <rect x="3" y="11" width="18" height="11" rx="2" ry="2"/>
              <path d="M7 11V7a5 5 0 0 1 10 0v4"/>
            </svg>
            <input
              v-model="password"
              :type="mostrarPassword ? 'text' : 'password'"
              class="input-base"
              placeholder="••••••••"
              @keyup.enter="ingresar"
            />
          </div>
          <button class="btn-toggle-pass" @click="mostrarPassword = !mostrarPassword">
            {{ mostrarPassword ? '🙈 Ocultar' : '👁️ Mostrar' }}
          </button>
        </div>

        <!-- Error -->
        <div class="login-error" v-if="errorMsg">
          ⚠️ {{ errorMsg }}
        </div>

        <!-- Botón -->
        <button
          class="btn-primary w-full mt-4"
          :disabled="cargando"
          @click="ingresar"
        >
          <span v-if="!cargando">Ingresar al sistema →</span>
          <span v-else class="spinner"></span>
        </button>

        <p class="login-footer-text">
          ¿Problemas para acceder?
          <a href="#" class="link-cyan">Contacta al administrador</a>
        </p>

      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { authService } from '../services/auth.js'

const router = useRouter()

const email           = ref('')
const password        = ref('')
const rolSeleccionado = ref('estudiante')
const cargando        = ref(false)
const errorMsg        = ref('')
const mostrarPassword = ref(false)

const roles = [
  { value: 'estudiante', label: 'Estudiante',   icono: '🎓' },
  { value: 'docente',    label: 'Docente',       icono: '👨‍🏫' },
  { value: 'admin',      label: 'Administrador', icono: '🗂️' },
  { value: 'superadmin', label: 'Super Admin',   icono: '⚙️' },
]

const rutasPorRol = {
  estudiante: '/estudiante/dashboard',
  docente:    '/docente/dashboard',
  admin:      '/admin/dashboard',
  superadmin: '/superadmin/dashboard',
}

const placeholderEmail = computed(() => {
  const map = {
    estudiante: 'usuario@est.umsa.bo',
    docente:    'docente@fcpn.umsa.bo',
    admin:      'admin@lasin.umsa.bo',
    superadmin: 'superadmin@lasin.umsa.bo',
  }
  return map[rolSeleccionado.value]
})

function validarFormulario() {
  if (!email.value.trim()) {
    errorMsg.value = 'El correo es obligatorio.'
    return false
  }
  if (!email.value.includes('@')) {
    errorMsg.value = 'Ingresa un correo válido.'
    return false
  }
  if (!password.value.trim()) {
    errorMsg.value = 'La contraseña es obligatoria.'
    return false
  }
  if (password.value.length < 6) {
    errorMsg.value = 'La contraseña debe tener al menos 6 caracteres.'
    return false
  }
  return true
}

async function ingresar() {
  errorMsg.value = ''
  if (!validarFormulario()) return

  cargando.value = true
  try {
    const data = await authService.login(email.value, password.value)
    const rol = data.rol
    const ruta = rutasPorRol[rol] || '/estudiante/dashboard'
    router.push(ruta)
  } catch (error) {
    if (error.response?.status === 401) {
      errorMsg.value = 'Correo o contraseña incorrectos.'
    } else if (error.response?.status === 403) {
      errorMsg.value = error.response.data.detail
    } else {
      errorMsg.value = 'Error al conectar con el servidor.'
    }
  } finally {
    cargando.value = false
  }
}
</script>

<style scoped>
.login-page {
  display: flex;
  min-height: 100vh;
  font-family: var(--font-main);
  background: var(--color-bg);
  color: var(--text-primary);
}

.login-hero {
  flex: 1;
  background:
    linear-gradient(135deg, rgba(0,119,182,0.15) 0%, rgba(0,212,255,0.05) 100%),
    var(--color-surface);
  border-right: 1px solid var(--border-subtle);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 60px 48px;
}

.hero-content    { max-width: 400px; }

.hero-logo {
  display: flex;
  align-items: center;
  gap: 14px;
  margin-bottom: 48px;
}

.hero-logo__title {
  display: block;
  font-size: 18px;
  font-weight: 800;
  letter-spacing: -0.3px;
}

.hero-logo__sub {
  font-size: 11px;
  color: var(--text-muted);
}

.hero-title {
  font-size: 38px;
  font-weight: 800;
  line-height: 1.2;
  margin-bottom: 18px;
  letter-spacing: -0.5px;
}

.hero-desc {
  font-size: 15px;
  color: var(--text-muted);
  line-height: 1.7;
  margin-bottom: 48px;
}

.hero-stats {
  display: flex;
  gap: 32px;
}

.hero-stat { display: flex; flex-direction: column; gap: 4px; }
.hero-stat__num   { font-size: 28px; font-weight: 800; line-height: 1; }
.hero-stat__label { font-size: 11px; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.5px; }

.login-form-wrap {
  width: 480px;
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 60px 48px;
}

.login-form { width: 100%; }
.form-head       { margin-bottom: 28px; }
.form-head h2    { font-size: 24px; font-weight: 700; margin-bottom: 6px; }

.role-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px;
  margin-bottom: 8px;
}

.role-btn {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
  padding: 14px 10px;
  background: rgba(255,255,255,0.03);
  border: 1px solid var(--border-soft);
  border-radius: var(--radius-lg);
  color: var(--text-muted);
  font-family: var(--font-main);
  cursor: pointer;
  transition: var(--transition-normal);
}

.role-btn:hover { border-color: rgba(0,212,255,0.25); color: var(--text-primary); }

.role-btn.active {
  background: rgba(0,119,182,0.15);
  border-color: var(--color-cyan);
  color: var(--color-cyan);
}

.role-btn__icon  { font-size: 22px; }
.role-btn__label { font-size: 12px; font-weight: 600; }

.mt-3 { margin-top: 14px; }
.mt-4 { margin-top: 20px; }
.w-full { width: 100%; }

.field-label {
  display: block;
  font-size: 13px;
  font-weight: 600;
  margin-bottom: 8px;
  color: var(--text-primary);
}

.search-wrap {
  display: flex;
  align-items: center;
  gap: 10px;
  background: rgba(255,255,255,0.05);
  border: 1px solid var(--border-soft);
  border-radius: 8px;
  padding: 10px 14px;
}

.input-base {
  background: transparent;
  border: none;
  outline: none;
  color: var(--text-primary);
  font-family: var(--font-main);
  font-size: 14px;
  width: 100%;
}

.btn-toggle-pass {
  margin-top: 6px;
  background: transparent;
  border: none;
  color: var(--text-muted);
  font-family: var(--font-main);
  font-size: 11px;
  cursor: pointer;
  padding: 0;
}

.btn-toggle-pass:hover { color: var(--color-cyan); }

.login-error {
  margin-top: 14px;
  padding: 12px 16px;
  background: rgba(239,68,68,0.08);
  border: 1px solid rgba(239,68,68,0.2);
  border-radius: 8px;
  color: #fca5a5;
  font-size: 13px;
}

.btn-primary {
  display: block;
  padding: 12px 24px;
  background: var(--color-cyan, #00d4ff);
  color: #000;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 700;
  cursor: pointer;
}

.btn-primary:disabled { opacity: 0.6; cursor: not-allowed; }

.spinner {
  display: inline-block;
  width: 18px;
  height: 18px;
  border: 2px solid rgba(255,255,255,0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.7s linear infinite;
}

@keyframes spin { to { transform: rotate(360deg); } }

.login-footer-text {
  margin-top: 20px;
  text-align: center;
  font-size: 12px;
  color: var(--text-muted);
}

.link-cyan {
  color: var(--color-cyan);
  text-decoration: none;
  font-weight: 600;
}

.text-cyan { color: var(--color-cyan, #00d4ff); }
.text-gold { color: #f59e0b; }
.text-success { color: #10b981; }
.text-muted { color: var(--text-muted, #888); }
</style>