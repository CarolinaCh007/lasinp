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
    // Estudiante
    {
      path: '/estudiante/dashboard',
      name: 'estudiante-dashboard',
      component: () => import('../views/estudiante/DashboardEstudiante.vue'),
      meta: { requiresAuth: true, rol: 'estudiante' }
    },
    // Docente
    {
      path: '/docente/dashboard',
      name: 'docente-dashboard',
      component: () => import('../views/docente/DashboardDocente.vue'),
      meta: { requiresAuth: true, rol: 'docente' }
    },
    // Admin
    {
      path: '/admin/dashboard',
      name: 'admin-dashboard',
      component: () => import('../views/admin/DashboardAdmin.vue'),
      meta: { requiresAuth: true, rol: 'admin' }
    },
    // Superadmin
    {
      path: '/superadmin/dashboard',
      name: 'superadmin-dashboard',
      component: () => import('../views/superadmin/DashboardSuperadmin.vue'),
      meta: { requiresAuth: true, rol: 'superadmin' }
    },
  ]
})

// Guard — protege rutas que requieren autenticación
router.beforeEach((to, from) => {
  if (to.meta.requiresAuth && !authService.estaAutenticado()) {
    return '/login'
  }
})

export default router