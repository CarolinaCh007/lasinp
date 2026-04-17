import { createRouter, createWebHistory } from 'vue-router'
import { authService } from '../services/auth.js'
import LoginView from '../views/LoginView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      redirect: '/login'
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView
    },

    // ── Estudiante ──────────────────────────────────────
    {
      path: '/estudiante/dashboard',
      component: () => import('../views/estudiante/DashboardView.vue'),
      meta: { requiresAuth: true, rol: 'estudiante' }
    },
    {
      path: '/estudiante/cursos',
      component: () => import('../views/estudiante/CursosView.vue'),
      meta: { requiresAuth: true, rol: 'estudiante' }
    },
    {
      path: '/estudiante/historial',
      component: () => import('../views/estudiante/HistorialView.vue'),
      meta: { requiresAuth: true, rol: 'estudiante' }
    },
    {
      path: '/estudiante/perfil',
      component: () => import('../views/estudiante/PerfilView.vue'),
      meta: { requiresAuth: true, rol: 'estudiante' }
    },

    // ── Docente ─────────────────────────────────────────
    {
      path: '/docente/dashboard',
      component: () => import('../views/docente/DashboardView.vue'),
      meta: { requiresAuth: true, rol: 'docente' }
    },
    {
      path: '/docente/estudiantes',
      component: () => import('../views/docente/EstudiantesView.vue'),
      meta: { requiresAuth: true, rol: 'docente' }
    },
    {
      path: '/docente/calificaciones',
      component: () => import('../views/docente/CalificacionesView.vue'),
      meta: { requiresAuth: true, rol: 'docente' }
    },
    {
      path: '/docente/comunicados',
      component: () => import('../views/docente/ComunicadosView.vue'),
      meta: { requiresAuth: true, rol: 'docente' }
    },

    // ── Admin ────────────────────────────────────────────
    {
      path: '/admin/dashboard',
      component: () => import('../views/admin/DashboardView.vue'),
      meta: { requiresAuth: true, rol: 'admin' }
    },
    {
      path: '/admin/preinscritos',
      component: () => import('../views/admin/PreinscritosView.vue'),
      meta: { requiresAuth: true, rol: 'admin' }
    },
    {
      path: '/admin/reportes',
      component: () => import('../views/admin/ReportesView.vue'),
      meta: { requiresAuth: true, rol: 'admin' }
    },

    // ── Superadmin ───────────────────────────────────────
    {
      path: '/superadmin/dashboard',
      component: () => import('../views/superadmin/DashboardView.vue'),
      meta: { requiresAuth: true, rol: 'superadmin' }
    },
    {
      path: '/superadmin/usuarios',
      component: () => import('../views/superadmin/UsuariosView.vue'),
      meta: { requiresAuth: true, rol: 'superadmin' }
    },
    {
      path: '/superadmin/cursos',
      component: () => import('../views/superadmin/CursosView.vue'),
      meta: { requiresAuth: true, rol: 'superadmin' }
    },
    {
      path: '/superadmin/reportes',
      component: () => import('../views/superadmin/ReportesView.vue'),
      meta: { requiresAuth: true, rol: 'superadmin' }
    },
    {
      path: '/superadmin/auditoria',
      component: () => import('../views/superadmin/AuditoriaView.vue'),
      meta: { requiresAuth: true, rol: 'superadmin' }
    },
  ]
})

router.beforeEach((to, from) => {
  if (to.meta.requiresAuth && !authService.estaAutenticado()) {
    return '/login'
  }
})

export default router