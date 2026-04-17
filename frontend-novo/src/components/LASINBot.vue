<template>
  <!-- ── FAB Botón flotante ─────────────────────────────── -->
  <button
    class="bot-fab"
    :class="{ active: abierto }"
    @click="abierto = !abierto"
    :title="abierto ? 'Cerrar chat' : 'Abrir asistente LASIN'"
  >
    <svg v-if="!abierto" width="24" height="24" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
      <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
    </svg>
    <svg v-else width="24" height="24" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
      <line x1="18" y1="6" x2="6" y2="18"/>
      <line x1="6" y1="6" x2="18" y2="18"/>
    </svg>
    <span v-if="mensajesNoLeidos > 0" class="bot-fab__badge">{{ mensajesNoLeidos }}</span>
  </button>

  <!-- ── Ventana del chat ───────────────────────────────── -->
  <Transition name="slide-up">
    <div v-if="abierto" class="bot-window">

      <!-- Header -->
      <div class="bot-header">
        <div class="bot-header__info">
          <div class="bot-avatar">🤖</div>
          <div>
            <strong>LASIN Bot</strong>
            <span class="bot-status">
              <span class="live-dot"></span>
              En línea
            </span>
          </div>
        </div>
        <button class="btn-close-modal" @click="abierto = false">✕</button>
      </div>

      <!-- Mensajes -->
      <div class="bot-messages" ref="messagesContainer">
        <div
          v-for="msg in mensajes"
          :key="msg.id"
          class="bot-msg"
          :class="msg.origen"
        >
          <div class="bot-msg__avatar" v-if="msg.origen === 'bot'">🤖</div>
          <div class="bot-msg__bubble">
            <span v-html="msg.texto"></span>
            <span class="bot-msg__time">{{ msg.hora }}</span>
          </div>
        </div>

        <!-- Indicador de escritura -->
        <div class="bot-msg bot" v-if="escribiendo">
          <div class="bot-msg__avatar">🤖</div>
          <div class="bot-msg__bubble typing">
            <span></span><span></span><span></span>
          </div>
        </div>
      </div>

      <!-- Sugerencias rápidas -->
      <div class="bot-suggestions" v-if="mostrarSugerencias">
        <button
          v-for="s in sugerenciasActuales"
          :key="s.label"
          class="bot-suggestion"
          @click="enviarSugerencia(s)"
        >
          {{ s.label }}
        </button>
      </div>

      <!-- Input -->
      <div class="bot-input">
        <input
          v-model="inputTexto"
          type="text"
          placeholder="Escribe tu pregunta..."
          class="bot-input__field"
          @keyup.enter="enviarMensaje"
          :disabled="escribiendo"
        />
        <button
          class="bot-input__btn"
          @click="enviarMensaje"
          :disabled="!inputTexto.trim() || escribiendo"
        >
          <svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
            <line x1="22" y1="2" x2="11" y2="13"/>
            <polygon points="22 2 15 22 11 13 2 9 22 2"/>
          </svg>
        </button>
      </div>

      <!-- Footer -->
      <div class="bot-footer">
        <!-- TODO: Conectar con API Flask + modelo de lenguaje en Fase 2 -->
        ⚡ LASIN Bot v1.0 · Respuestas automáticas
      </div>

    </div>
  </Transition>
</template>

<script setup>
// ─── Imports ────────────────────────────────────────────────
import { ref, nextTick, computed } from 'vue'

// ─── Estado ─────────────────────────────────────────────────
const abierto            = ref(false)
const inputTexto         = ref('')
const escribiendo        = ref(false)
const mostrarSugerencias = ref(true)
const mensajesNoLeidos   = ref(1)
const messagesContainer  = ref(null)

// ─── Historial de mensajes ───────────────────────────────────
const mensajes = ref([
  {
    id: 1,
    origen: 'bot',
    texto: '¡Hola! 👋 Soy el <strong>asistente virtual del LASIN</strong>. Puedo ayudarte con información sobre cursos, inscripciones, costos y más. ¿En qué te puedo ayudar?',
    hora: horaActual(),
  }
])

// ─── Sugerencias por contexto ────────────────────────────────
const sugerenciasIniciales = [
  { label: '📚 Ver cursos disponibles', intent: 'cursos'        },
  { label: '📅 Fechas de inscripción',  intent: 'inscripcion'   },
  { label: '💰 Información de costos',  intent: 'costos'        },
  { label: '📍 Ubicación del LASIN',    intent: 'ubicacion'     },
  { label: '📞 Contacto',               intent: 'contacto'      },
]

const sugerenciasActuales = ref([...sugerenciasIniciales])

// ─── Base de conocimiento LASIN ──────────────────────────────
/**
 * Cada entrada tiene:
 * - keywords: palabras clave que activan esta respuesta
 * - respuesta: texto HTML de respuesta
 * - sugerencias: opciones de seguimiento
 *
 * TODO: En Fase 2, reemplazar por llamada a la API Flask
 * que procesará el mensaje con un modelo de lenguaje (NLP).
 */
const conocimiento = [
  {
    keywords: ['curso', 'cursos', 'oferta', 'que ofrecen', 'disponible', 'programas'],
    respuesta: `📚 <strong>Cursos disponibles en LASIN 2025:</strong><br><br>
      🐍 <strong>Python para Data Science</strong> — Bs. 350 · 3 meses<br>
      ⚛️ <strong>React & Angular Avanzado</strong> — Bs. 400 · 4 meses<br>
      🤖 <strong>Machine Learning Aplicado</strong> — Bs. 480 · 4 meses<br>
      🔐 <strong>Ethical Hacking</strong> — Bs. 450 · 3 meses<br>
      ☁️ <strong>Azure Fundamentals</strong> — Bs. 380 · 2 meses<br>
      📊 <strong>Excel & Power BI</strong> — Bs. 250 · 2 meses<br><br>
      ¿Te interesa alguno en particular?`,
    sugerencias: [
      { label: '📅 ¿Cuándo empieza?',    intent: 'inicio'      },
      { label: '💰 ¿Cuánto cuesta?',     intent: 'costos'      },
      { label: '📝 Quiero inscribirme',   intent: 'inscripcion' },
    ]
  },
  {
    keywords: ['inscripcion', 'inscribir', 'preinscripcion', 'registrar', 'como me inscribo', 'cuando'],
    respuesta: `📝 <strong>Proceso de inscripción:</strong><br><br>
      1️⃣ Regístrate en la plataforma<br>
      2️⃣ Selecciona tu curso de interés<br>
      3️⃣ Haz clic en <em>"Preinscripción"</em><br>
      4️⃣ Realiza el pago en las oficinas del LASIN<br>
      5️⃣ El admin confirmará tu inscripción<br><br>
      📅 <strong>Próxima apertura:</strong> Marzo 2025<br>
      ⏰ <strong>Horario de atención:</strong> Lun–Vie 8:00–18:00`,
    sugerencias: [
      { label: '💰 Ver costos',           intent: 'costos'    },
      { label: '📍 ¿Dónde pago?',        intent: 'ubicacion' },
      { label: '📚 Ver cursos',           intent: 'cursos'    },
    ]
  },
  {
    keywords: ['costo', 'costos', 'precio', 'cuanto', 'cuánto', 'pago', 'pagar', 'vale'],
    respuesta: `💰 <strong>Precios por curso:</strong><br><br>
      • Excel & Power BI → <strong>Bs. 250</strong><br>
      • Python Data Science → <strong>Bs. 350</strong><br>
      • Azure Fundamentals → <strong>Bs. 380</strong><br>
      • React & Angular → <strong>Bs. 400</strong><br>
      • Ethical Hacking → <strong>Bs. 450</strong><br>
      • Machine Learning → <strong>Bs. 480</strong><br><br>
      💳 El pago se realiza <strong>en efectivo</strong> en las oficinas del LASIN.`,
    sugerencias: [
      { label: '📝 Inscribirme ahora',   intent: 'inscripcion' },
      { label: '📍 ¿Dónde están?',      intent: 'ubicacion'   },
      { label: '📚 Ver todos los cursos',intent: 'cursos'      },
    ]
  },
  {
    keywords: ['ubicacion', 'donde', 'dónde', 'direccion', 'dirección', 'lugar', 'llegar'],
    respuesta: `📍 <strong>Ubicación del LASIN:</strong><br><br>
      🏛️ Facultad de Ciencias Puras y Naturales<br>
      Universidad Mayor de San Andrés (UMSA)<br>
      Av. Villazón, La Paz, Bolivia<br><br>
      🕐 <strong>Atención:</strong> Lun–Vie 8:00–18:00<br>
      📞 <strong>Tel:</strong> +591 2 xxx-xxxx<br>
      📧 <strong>Email:</strong> info@lasin.umsa.bo`,
    sugerencias: [
      { label: '📞 Contactar ahora',  intent: 'contacto'    },
      { label: '📚 Ver cursos',       intent: 'cursos'      },
      { label: '📝 Inscribirme',      intent: 'inscripcion' },
    ]
  },
  {
    keywords: ['contacto', 'contactar', 'telefono', 'teléfono', 'email', 'correo', 'llamar', 'comunicar'],
    respuesta: `📞 <strong>Contacto LASIN:</strong><br><br>
      📧 info@lasin.umsa.bo<br>
      📱 +591 2 xxx-xxxx (WhatsApp)<br>
      💬 Facebook: /LASINInformatica<br>
      📸 Instagram: @lasin_umsa<br><br>
      ⏰ Respuesta en horario hábil: Lun–Vie 8:00–18:00`,
    sugerencias: [
      { label: '📚 Ver cursos',     intent: 'cursos'    },
      { label: '📍 Ubicación',     intent: 'ubicacion' },
    ]
  },
  {
    keywords: ['horario', 'hora', 'turno', 'mañana', 'tarde', 'noche', 'cuando son'],
    respuesta: `🕐 <strong>Horarios de clases:</strong><br><br>
      🌅 <strong>Mañana:</strong> 08:00 – 10:00<br>
      ☀️ <strong>Mediodía:</strong> 10:00 – 12:00<br>
      🌆 <strong>Tarde:</strong> 14:00 – 16:00 / 16:00 – 18:00<br>
      🌙 <strong>Noche:</strong> 18:00 – 20:00<br><br>
      El horario exacto depende del curso. ¿Quieres info de uno específico?`,
    sugerencias: [
      { label: '📚 Ver cursos',     intent: 'cursos'    },
      { label: '📝 Inscribirme',   intent: 'inscripcion'},
    ]
  },
  {
    keywords: ['certificado', 'certificacion', 'diploma', 'titulo', 'título', 'acreditado'],
    respuesta: `🏆 <strong>Certificaciones LASIN:</strong><br><br>
      ✅ Todos los cursos otorgan <strong>certificado oficial</strong> de la UMSA<br>
      ✅ Carrera de Informática acreditada<br>
      ✅ Reconocido a nivel nacional<br><br>
      📋 <strong>Requisito:</strong> Asistencia mínima del 80% y nota ≥ 60/100<br>
      📥 El certificado se descarga desde tu perfil digital`,
    sugerencias: [
      { label: '📚 Ver cursos',     intent: 'cursos'    },
      { label: '📝 Inscribirme',   intent: 'inscripcion'},
    ]
  },
  {
    keywords: ['inicio', 'empieza', 'comienza', 'fecha', 'cuándo empieza', 'cuando empieza'],
    respuesta: `📅 <strong>Fechas de inicio — Ciclo 2025:</strong><br><br>
      🟢 <strong>Grupo A:</strong> 01 de Marzo 2025<br>
      🟢 <strong>Grupo B:</strong> 15 de Marzo 2025<br>
      🟡 <strong>Grupo C:</strong> 01 de Abril 2025<br><br>
      ⚠️ Cupos limitados — ¡Se llenan rápido!<br>
      📝 Preinscríbete hoy para asegurar tu lugar.`,
    sugerencias: [
      { label: '📝 Inscribirme ahora', intent: 'inscripcion' },
      { label: '💰 Ver costos',        intent: 'costos'      },
    ]
  },
]

// ─── Respuesta por defecto ────────────────────────────────────
const respuestaDefault = `🤔 No entendí bien tu pregunta. Puedo ayudarte con:<br><br>
  📚 Cursos disponibles<br>
  📅 Fechas de inscripción<br>
  💰 Costos y pagos<br>
  📍 Ubicación<br>
  📞 Contacto<br><br>
  ¿Sobre qué te gustaría saber más?`

// ─── Funciones auxiliares ────────────────────────────────────

/** Devuelve la hora actual formateada HH:MM */
function horaActual() {
  return new Date().toLocaleTimeString('es-BO', { hour: '2-digit', minute: '2-digit' })
}

/** Busca en la base de conocimiento por keywords */
function buscarRespuesta(texto) {
  const textoLower = texto.toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '')

  for (const entrada of conocimiento) {
    const encontrado = entrada.keywords.some(kw =>
      textoLower.includes(kw.normalize('NFD').replace(/[\u0300-\u036f]/g, ''))
    )
    if (encontrado) return entrada
  }
  return null
}

/** Hace scroll al último mensaje */
async function scrollAbajo() {
  await nextTick()
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
  }
}

// ─── Lógica principal ────────────────────────────────────────

/**
 * Procesa un mensaje del usuario y genera respuesta del bot.
 * TODO: En Fase 2, reemplazar `buscarRespuesta()` por:
 *   const respuesta = await fetch('/api/chatbot', {
 *     method: 'POST',
 *     body: JSON.stringify({ mensaje: texto })
 *   }).then(r => r.json())
 */
async function procesarMensaje(texto) {
  mostrarSugerencias.value = false
  escribiendo.value = true
  await scrollAbajo()

  // Simulamos delay de respuesta (en Fase 2 → await API call)
  await new Promise(resolve => setTimeout(resolve, 800 + Math.random() * 600))

  const entrada = buscarRespuesta(texto)
  const respuesta = entrada ? entrada.respuesta : respuestaDefault
  const siguientesSugerencias = entrada?.sugerencias || sugerenciasIniciales

  escribiendo.value = false

  mensajes.value.push({
    id: Date.now(),
    origen: 'bot',
    texto: respuesta,
    hora: horaActual(),
  })

  sugerenciasActuales.value = siguientesSugerencias
  mostrarSugerencias.value = true
  await scrollAbajo()
}

/** Envía mensaje escrito por el usuario */
async function enviarMensaje() {
  const texto = inputTexto.value.trim()
  if (!texto || escribiendo.value) return

  mensajes.value.push({
    id: Date.now(),
    origen: 'usuario',
    texto,
    hora: horaActual(),
  })

  inputTexto.value = ''
  mensajesNoLeidos.value = 0
  await scrollAbajo()
  await procesarMensaje(texto)
}

/** Envía una sugerencia predefinida */
async function enviarSugerencia(sugerencia) {
  mensajes.value.push({
    id: Date.now(),
    origen: 'usuario',
    texto: sugerencia.label,
    hora: horaActual(),
  })

  mensajesNoLeidos.value = 0
  mostrarSugerencias.value = false
  await scrollAbajo()

  // Buscamos por intent directamente
  const entrada = conocimiento.find(e => e.keywords.includes(sugerencia.intent))
  await procesarMensaje(sugerencia.intent)
}
</script>

<style scoped>
/* ── FAB ─────────────────────────────────────────────────── */
.bot-fab {
  position: fixed;
  bottom: 32px;
  right: 32px;
  width: 58px;
  height: 58px;
  border-radius: 50%;
  background: linear-gradient(135deg, #0077b6, #00b4d8);
  border: none;
  color: white;
  cursor: pointer;
  box-shadow: 0 8px 24px rgba(0,119,182,0.5);
  transition: all 0.3s;
  z-index: 1000;
  display: flex;
  align-items: center;
  justify-content: center;
}

.bot-fab:hover  { transform: scale(1.08); box-shadow: 0 12px 32px rgba(0,119,182,0.6); }
.bot-fab.active { background: #ef4444; box-shadow: 0 8px 24px rgba(239,68,68,0.5); }

.bot-fab__badge {
  position: absolute;
  top: -4px;
  right: -4px;
  width: 20px;
  height: 20px;
  background: #ef4444;
  border-radius: 50%;
  font-size: 11px;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 2px solid #0d1b2e;
}

/* ── Ventana ─────────────────────────────────────────────── */
.bot-window {
  position: fixed;
  bottom: 104px;
  right: 32px;
  width: 370px;
  max-height: 580px;
  background: #0a1628;
  border: 1px solid rgba(0,212,255,0.15);
  border-radius: 20px;
  box-shadow: 0 24px 60px rgba(0,0,0,0.5);
  z-index: 999;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  font-family: 'Sora', sans-serif;
}

/* ── Header ──────────────────────────────────────────────── */
.bot-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
  background: linear-gradient(135deg, #0077b6, #005f99);
  border-bottom: 1px solid rgba(0,212,255,0.1);
  flex-shrink: 0;
}

.bot-header__info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.bot-avatar {
  width: 38px;
  height: 38px;
  background: rgba(255,255,255,0.15);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
}

.bot-header__info strong { display: block; font-size: 14px; font-weight: 700; }

.bot-status {
  display: flex;
  align-items: center;
  gap: 5px;
  font-size: 11px;
  color: rgba(255,255,255,0.75);
}

.live-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: #22c55e;
  animation: pulse 1.5s infinite;
}

@keyframes pulse { 0%,100%{opacity:1;transform:scale(1)} 50%{opacity:0.5;transform:scale(1.3)} }

.btn-close-modal {
  background: rgba(255,255,255,0.15);
  border: none;
  color: white;
  width: 28px;
  height: 28px;
  border-radius: 50%;
  font-size: 13px;
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
}

.btn-close-modal:hover { background: rgba(255,255,255,0.3); }

/* ── Mensajes ────────────────────────────────────────────── */
.bot-messages {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 12px;
  background: #0d1b2e;
  scrollbar-width: thin;
  scrollbar-color: rgba(0,212,255,0.2) transparent;
}

.bot-msg {
  display: flex;
  gap: 8px;
  align-items: flex-end;
}

.bot-msg.usuario {
  flex-direction: row-reverse;
}

.bot-msg__avatar {
  width: 30px;
  height: 30px;
  background: rgba(0,212,255,0.1);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  flex-shrink: 0;
}

.bot-msg__bubble {
  max-width: 78%;
  padding: 10px 14px;
  border-radius: 16px;
  font-size: 12.5px;
  line-height: 1.6;
  position: relative;
}

.bot-msg.bot .bot-msg__bubble {
  background: #0a1628;
  border: 1px solid rgba(0,212,255,0.1);
  border-bottom-left-radius: 4px;
}

.bot-msg.usuario .bot-msg__bubble {
  background: linear-gradient(135deg, #0077b6, #00b4d8);
  color: white;
  border-bottom-right-radius: 4px;
}

.bot-msg__time {
  display: block;
  font-size: 9px;
  color: rgba(255,255,255,0.4);
  margin-top: 4px;
  text-align: right;
}

.bot-msg.bot .bot-msg__time { color: #4a6080; }

/* ── Typing indicator ────────────────────────────────────── */
.bot-msg__bubble.typing {
  display: flex;
  gap: 4px;
  align-items: center;
  padding: 14px 18px;
}

.bot-msg__bubble.typing span {
  width: 6px;
  height: 6px;
  background: #00d4ff;
  border-radius: 50%;
  animation: typing 1.2s infinite;
}

.bot-msg__bubble.typing span:nth-child(2) { animation-delay: 0.2s; }
.bot-msg__bubble.typing span:nth-child(3) { animation-delay: 0.4s; }

@keyframes typing { 0%,60%,100%{opacity:0.3;transform:translateY(0)} 30%{opacity:1;transform:translateY(-4px)} }

/* ── Sugerencias ─────────────────────────────────────────── */
.bot-suggestions {
  padding: 10px 14px;
  display: flex;
  flex-direction: column;
  gap: 6px;
  border-top: 1px solid rgba(0,212,255,0.08);
  background: #0d1b2e;
  flex-shrink: 0;
}

.bot-suggestion {
  background: rgba(255,255,255,0.03);
  border: 1px solid rgba(0,212,255,0.1);
  border-radius: 9px;
  padding: 8px 12px;
  text-align: left;
  font-size: 12px;
  font-family: 'Sora', sans-serif;
  color: #f0f8ff;
  cursor: pointer;
  transition: all 0.2s;
}

.bot-suggestion:hover {
  background: rgba(0,212,255,0.08);
  border-color: rgba(0,212,255,0.25);
  transform: translateX(3px);
}

/* ── Input ───────────────────────────────────────────────── */
.bot-input {
  display: flex;
  gap: 8px;
  padding: 12px 14px;
  border-top: 1px solid rgba(0,212,255,0.08);
  background: #0a1628;
  flex-shrink: 0;
}

.bot-input__field {
  flex: 1;
  padding: 10px 14px;
  background: rgba(255,255,255,0.05);
  border: 1px solid rgba(255,255,255,0.08);
  border-radius: 10px;
  color: #f0f8ff;
  font-family: 'Sora', sans-serif;
  font-size: 13px;
  outline: none;
  transition: all 0.2s;
}

.bot-input__field:focus       { border-color: rgba(0,212,255,0.4); }
.bot-input__field::placeholder { color: #4a6080; }
.bot-input__field:disabled    { opacity: 0.5; }

.bot-input__btn {
  width: 40px;
  height: 40px;
  background: linear-gradient(135deg, #0077b6, #00b4d8);
  border: none;
  border-radius: 10px;
  color: white;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
  flex-shrink: 0;
}

.bot-input__btn:hover:not(:disabled) { box-shadow: 0 4px 14px rgba(0,180,216,0.4); }
.bot-input__btn:disabled { opacity: 0.4; cursor: not-allowed; }

/* ── Footer ──────────────────────────────────────────────── */
.bot-footer {
  padding: 8px 14px;
  font-size: 10px;
  color: #4a6080;
  text-align: center;
  background: #0a1628;
  border-top: 1px solid rgba(0,212,255,0.05);
  flex-shrink: 0;
}

/* ── Transición ──────────────────────────────────────────── */
.slide-up-enter-active, .slide-up-leave-active { transition: all 0.3s ease; }
.slide-up-enter-from, .slide-up-leave-to { opacity: 0; transform: translateY(20px) scale(0.97); }

/* ── Responsive ──────────────────────────────────────────── */
@media (max-width: 480px) {
  .bot-window { width: calc(100vw - 48px); right: 24px; }
}
</style>