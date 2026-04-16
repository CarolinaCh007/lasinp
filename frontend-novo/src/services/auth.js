import axios from 'axios'

const API_URL = 'http://127.0.0.1:8000'

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json'
  }
})

// Interceptor — agrega el token automáticamente a cada petición
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

export const authService = {
  async login(correo_electronico, password) {
    const response = await api.post('/auth/login', {
      correo_electronico,
      password
    })
    // Guardar token y datos del usuario
    localStorage.setItem('token', response.data.access_token)
    localStorage.setItem('usuario', JSON.stringify(response.data.usuario))
    localStorage.setItem('rol', response.data.rol)
    return response.data
  },

  logout() {
    localStorage.removeItem('token')
    localStorage.removeItem('usuario')
    localStorage.removeItem('rol')
  },

  getToken() {
    return localStorage.getItem('token')
  },

  getUsuario() {
    const u = localStorage.getItem('usuario')
    return u ? JSON.parse(u) : null
  },

  getRol() {
    return localStorage.getItem('rol')
  },

  estaAutenticado() {
    return !!localStorage.getItem('token')
  }
}

export default api