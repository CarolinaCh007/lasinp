import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router/index.js'

// Estilos globales
import './assets/css/variables.css'
import './assets/css/animations.css'
import './assets/css/components.css'
import './assets/css/utilities.css'

const app = createApp(App)

app.use(createPinia())
app.use(router)

app.mount('#app')