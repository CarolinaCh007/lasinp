<template>
  <div>
    <h1>Dashboard Estudiante</h1>
    <p>Bienvenido estudiante</p>
    <button @click="cerrarSesion">Cerrar sesión</button>
  </div>
</template>

<script setup>
import { authService } from '../../services/auth.js'
import { useRouter } from 'vue-router'

const router = useRouter()

function cerrarSesion() {
  authService.logout()
  router.push('/login')
}
</script>