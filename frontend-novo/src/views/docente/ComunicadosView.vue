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
        <router-link to="/docente/dashboard"      class="nav-item">
          <svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="1.8" viewBox="0 0 24 24"><rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/></svg>
          Dashboard
        </router-link>
        <router-link to="/docente/estudiantes"    class="nav-item">
          <svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="1.8" viewBox="0 0 24 24"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>
          Mis Estudiantes
        </router-link>
        <router-link to="/docente/calificaciones" class="nav-item">
          <svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="1.8" viewBox="0 0 24 24"><path d="M12 20h9"/><path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"/></svg>
          Calificaciones
        </router-link>
        <router-link to="/docente/comunicados"    class="nav-item">
          <svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="1.8" viewBox="0 0 24 24"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>
          Comunicados
        </router-link>
      </nav>
      <div class="sidebar-footer">
        <div class="user-info">
          <div class="user-avatar">HM</div>
          <div><strong>Lic. H. Mamani</strong><span>Docente</span></div>
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
          <h1>Comunicados</h1>
          <p>Envía mensajes y recordatorios a tus estudiantes</p>
        </div>
      </div>

      <div class="two-col">

        <!-- Formulario nuevo comunicado -->
        <div class="panel">
          <div class="panel-header">
            <h2>✉️ Nuevo comunicado</h2>
          </div>

          <div class="field">
            <label>Destinatarios</label>
            <div class="dest-tabs">
              <button
                v-for="d in destinatarios" :key="d.value"
                class="dest-tab"
                :class="{ active: destActivo === d.value }"
                @click="destActivo = d.value"
              >{{ d.label }}</button>
            </div>
          </div>

          <div class="field" v-if="destActivo === 'curso'">
            <label>Seleccionar curso</label>
            <select v-model="form.cursoId" class="select-input">
              <option v-for="c in cursos" :key="c.id" :value="c.id">{{ c.nombre }}</option>
            </select>
          </div>

          <div class="field">
            <label>Tipo de comunicado</label>
            <div class="tipo-tabs">
              <button
                v-for="t in tipos" :key="t.value"
                class="tipo-tab"
                :class="[{ active: form.tipo === t.value }, t.value]"
                @click="form.tipo = t.value"
              >{{ t.icono }} {{ t.label }}</button>
            </div>
          </div>

          <div class="field">
            <label>Asunto</label>
            <input v-model="form.asunto" type="text" class="text-input" placeholder="Ej: Recordatorio de examen parcial"/>
          </div>

          <div class="field">
            <label>Mensaje</label>
            <textarea v-model="form.mensaje" class="textarea-input" rows="5" placeholder="Escribe el mensaje para tus estudiantes..."></textarea>
          </div>

          <div class="field">
            <label>Programar envío (opcional)</label>
            <input v-model="form.fecha" type="datetime-local" class="text-input"/>
          </div>

          <div class="form-footer-btns">
            <button class="btn-preview" @click="previsualizarComunicado">
              👁 Previsualizar
            </button>
            <button class="btn-enviar" @click="enviarComunicado" :disabled="enviando">
              <span v-if="enviando">Enviando...</span>
              <span v-else>📤 Enviar comunicado</span>
            </button>
          </div>

          <div class="alert-success" v-if="enviado">
            ✅ Comunicado enviado correctamente a {{ contadorDestinatarios }} estudiantes.
          </div>
        </div>

        <!-- Historial de comunicados -->
        <div class="panel">
          <div class="panel-header">
            <h2>📋 Historial</h2>
            <span class="badge-count">{{ comunicados.length }}</span>
          </div>

          <div class="comunicado-item" v-for="com in comunicados" :key="com.id">
            <div class="com-icon" :class="com.tipo">{{ iconoTipo(com.tipo) }}</div>
            <div class="com-info">
              <strong>{{ com.asunto }}</strong>
              <span class="com-dest">{{ com.destLabel }} · {{ com.fecha }}</span>
              <p class="com-preview">{{ com.mensaje.slice(0, 80) }}...</p>
            </div>
            <div class="com-meta">
              <span class="com-enviados">{{ com.enviados }} enviados</span>
              <span class="badge-tipo" :class="com.tipo">{{ com.tipo }}</span>
            </div>
          </div>
        </div>

      </div>
    </main>

    <!-- Modal previsualización -->
    <div class="modal-overlay" v-if="modalPreview" @click="modalPreview = false">
      <div class="modal" @click.stop>
        <div class="modal-header">
          <h2>Previsualización del comunicado</h2>
          <button class="btn-cerrar-modal" @click="modalPreview = false">✕</button>
        </div>
        <div class="email-preview">
          <div class="email-header">
            <div class="email-logo">LASIN · UMSA</div>
            <div class="email-badge" :class="form.tipo">{{ iconoTipo(form.tipo) }} {{ form.tipo }}</div>
          </div>
          <div class="email-body">
            <h3>{{ form.asunto || 'Sin asunto' }}</h3>
            <p>{{ form.mensaje || 'Sin mensaje.' }}</p>
          </div>
          <div class="email-footer">
            Lic. Henry Mamani · LASIN · Universidad Mayor de San Andrés
          </div>
        </div>
        <div class="modal-btns">
          <button class="btn-cancelar" @click="modalPreview = false">Cancelar</button>
          <button class="btn-confirmar" @click="confirmarEnvio">Confirmar y enviar</button>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const enviando    = ref(false)
const enviado     = ref(false)
const modalPreview = ref(false)
const destActivo  = ref('curso')

const form = ref({
  cursoId: 1,
  tipo:    'recordatorio',
  asunto:  '',
  mensaje: '',
  fecha:   '',
})

const cursos = ref([
  { id: 1, nombre: 'Python Data Science', inscritos: 28 },
  { id: 2, nombre: 'Machine Learning',     inscritos: 22 },
  { id: 3, nombre: 'Intro a la IA',        inscritos: 17 },
])

const destinatarios = [
  { value: 'curso',  label: '📚 Un curso específico' },
  { value: 'todos',  label: '👥 Todos mis cursos'    },
]

const tipos = [
  { value: 'recordatorio', label: 'Recordatorio', icono: '🔔' },
  { value: 'aviso',        label: 'Aviso',        icono: '📢' },
  { value: 'examen',       label: 'Examen',       icono: '📝' },
  { value: 'tarea',        label: 'Tarea',        icono: '📌' },
]

const comunicados = ref([
  { id: 1, asunto: 'Recordatorio examen parcial', tipo: 'examen',       destLabel: 'Python Data Science', fecha: '18/02/2025', enviados: 28, mensaje: 'El examen parcial se realizará el viernes 21 de febrero a las 08:00 en el Lab 3.' },
  { id: 2, asunto: 'Entrega de trabajo final',     tipo: 'tarea',        destLabel: 'Machine Learning',    fecha: '15/02/2025', enviados: 22, mensaje: 'El trabajo final debe entregarse antes del 28 de febrero vía el sistema LASIN.' },
  { id: 3, asunto: 'Clase suspendida',             tipo: 'aviso',        destLabel: 'Todos los cursos',    fecha: '10/02/2025', enviados: 67, mensaje: 'La clase del martes 11 de febrero queda suspendida por reunión docente.' },
  { id: 4, asunto: 'Materiales del módulo 3',      tipo: 'recordatorio', destLabel: 'Intro a la IA',       fecha: '05/02/2025', enviados: 17, mensaje: 'Los materiales del módulo 3 ya están disponibles en el aula virtual de Teams.' },
])

const contadorDestinatarios = computed(() => {
  if (destActivo.value === 'todos') return cursos.value.reduce((s, c) => s + c.inscritos, 0)
  return cursos.value.find(c => c.id === form.value.cursoId)?.inscritos ?? 0
})

function iconoTipo(tipo) {
  return { recordatorio: '🔔', aviso: '📢', examen: '📝', tarea: '📌' }[tipo] ?? '📩'
}

function previsualizarComunicado() {
  if (!form.value.asunto || !form.value.mensaje) {
    alert('Por favor completa el asunto y el mensaje.')
    return
  }
  modalPreview.value = true
}

async function enviarComunicado() {
  if (!form.value.asunto || !form.value.mensaje) {
    alert('Por favor completa el asunto y el mensaje.')
    return
  }
  enviando.value = true
  await new Promise(r => setTimeout(r, 1500))

  // Agregar al historial
  comunicados.value.unshift({
    id:        Date.now(),
    asunto:    form.value.asunto,
    tipo:      form.value.tipo,
    destLabel: destActivo.value === 'todos'
      ? 'Todos los cursos'
      : cursos.value.find(c => c.id === form.value.cursoId)?.nombre,
    fecha:    new Date().toLocaleDateString('es-BO'),
    enviados: contadorDestinatarios.value,
    mensaje:  form.value.mensaje,
  })

  // Resetear form
  form.value = { cursoId: 1, tipo: 'recordatorio', asunto: '', mensaje: '', fecha: '' }
  enviando.value = false
  enviado.value  = true
  setTimeout(() => enviado.value = false, 3000)
}

function confirmarEnvio() {
  modalPreview.value = false
  enviarComunicado()
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;500;600;700&display=swap');
* { box-sizing: border-box; margin: 0; padding: 0; }

.dashboard { font-family: 'Sora', sans-serif; display: flex; min-height: 100vh; background: #0d1b2e; color: #f0f8ff; }

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
.user-avatar { width: 36px; height: 36px; border-radius: 50%; background: linear-gradient(135deg, #0077b6, #ffd700); display: flex; align-items: center; justify-content: center; font-size: 12px; font-weight: 700; flex-shrink: 0; }
.user-info strong { display: block; font-size: 13px; }
.user-info span { font-size: 11px; color: #7a96b0; }
.btn-logout { width: 100%; display: flex; align-items: center; gap: 8px; padding: 9px 14px; background: transparent; border: 1px solid rgba(255,255,255,0.07); border-radius: 8px; color: #7a96b0; font-family: 'Sora', sans-serif; font-size: 13px; cursor: pointer; transition: all 0.2s; }
.btn-logout:hover { border-color: rgba(239,68,68,0.4); color: #fca5a5; }

.main { flex: 1; padding: 36px 40px; overflow-y: auto; }
.top-bar { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 24px; }
.top-bar h1 { font-size: 26px; font-weight: 700; margin-bottom: 4px; }
.top-bar p { font-size: 14px; color: #7a96b0; }

.two-col { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }

.panel { background: #0a1628; border: 1px solid rgba(0,212,255,0.08); border-radius: 16px; overflow: hidden; }
.panel-header { display: flex; justify-content: space-between; align-items: center; padding: 18px 20px; border-bottom: 1px solid rgba(0,212,255,0.08); }
.panel-header h2 { font-size: 15px; font-weight: 600; }
.badge-count { background: rgba(0,212,255,0.15); color: #00d4ff; font-size: 12px; font-weight: 700; padding: 2px 10px; border-radius: 100px; }

.field { padding: 0 20px; margin-bottom: 18px; }
.field:first-of-type { margin-top: 20px; }
.field label { display: block; font-size: 11px; font-weight: 600; color: #7a96b0; text-transform: uppercase; letter-spacing: 0.8px; margin-bottom: 8px; }

.dest-tabs { display: flex; gap: 8px; }
.dest-tab { flex: 1; padding: 9px; background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.07); border-radius: 10px; color: #7a96b0; font-family: 'Sora', sans-serif; font-size: 12px; cursor: pointer; transition: all 0.2s; text-align: center; }
.dest-tab:hover { border-color: rgba(0,212,255,0.2); color: #f0f8ff; }
.dest-tab.active { background: rgba(0,119,182,0.2); border-color: rgba(0,212,255,0.35); color: #00d4ff; }

.tipo-tabs { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; }
.tipo-tab { padding: 8px; background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.07); border-radius: 10px; color: #7a96b0; font-family: 'Sora', sans-serif; font-size: 12px; cursor: pointer; transition: all 0.2s; text-align: center; }
.tipo-tab:hover { color: #f0f8ff; }
.tipo-tab.active.recordatorio { background: rgba(0,212,255,0.15); border-color: rgba(0,212,255,0.35); color: #00d4ff; }
.tipo-tab.active.aviso  { background: rgba(168,85,247,0.15); border-color: rgba(168,85,247,0.35); color: #a855f7; }
.tipo-tab.active.examen { background: rgba(239,68,68,0.15);  border-color: rgba(239,68,68,0.35);  color: #f87171; }
.tipo-tab.active.tarea  { background: rgba(255,215,0,0.15);  border-color: rgba(255,215,0,0.35);  color: #ffd700; }

.select-input { width: 100%; padding: 11px 14px; background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.08); border-radius: 10px; color: #f0f8ff; font-family: 'Sora', sans-serif; font-size: 13px; outline: none; }
.select-input option { background: #0a1628; }

.text-input { width: 100%; padding: 11px 14px; background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.08); border-radius: 10px; color: #f0f8ff; font-family: 'Sora', sans-serif; font-size: 13px; outline: none; transition: all 0.2s; }
.text-input:focus { border-color: rgba(0,212,255,0.4); background: rgba(0,119,182,0.08); }
.text-input::placeholder { color: #7a96b0; }

.textarea-input { width: 100%; padding: 12px 14px; background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.08); border-radius: 10px; color: #f0f8ff; font-family: 'Sora', sans-serif; font-size: 13px; outline: none; resize: vertical; transition: all 0.2s; line-height: 1.6; }
.textarea-input:focus { border-color: rgba(0,212,255,0.4); background: rgba(0,119,182,0.08); }
.textarea-input::placeholder { color: #7a96b0; }

.form-footer-btns { display: flex; gap: 10px; padding: 0 20px; margin-bottom: 16px; }
.btn-preview { flex: 1; padding: 12px; background: transparent; border: 1px solid rgba(255,255,255,0.1); border-radius: 10px; color: #7a96b0; font-family: 'Sora', sans-serif; font-size: 13px; font-weight: 500; cursor: pointer; transition: all 0.2s; }
.btn-preview:hover { border-color: rgba(0,212,255,0.3); color: #00d4ff; }
.btn-enviar { flex: 2; padding: 12px; background: linear-gradient(135deg, #0077b6, #00b4d8); border: none; border-radius: 10px; color: white; font-family: 'Sora', sans-serif; font-size: 13px; font-weight: 600; cursor: pointer; transition: all 0.2s; }
.btn-enviar:hover:not(:disabled) { box-shadow: 0 6px 20px rgba(0,180,216,0.35); }
.btn-enviar:disabled { opacity: 0.6; cursor: not-allowed; }

.alert-success { margin: 0 20px 20px; background: rgba(34,197,94,0.1); border: 1px solid rgba(34,197,94,0.25); color: #86efac; border-radius: 10px; padding: 12px 16px; font-size: 13px; }

/* Historial */
.comunicado-item { display: flex; align-items: flex-start; gap: 14px; padding: 16px 20px; border-bottom: 1px solid rgba(255,255,255,0.04); transition: background 0.15s; }
.comunicado-item:last-child { border-bottom: none; }
.comunicado-item:hover { background: rgba(0,212,255,0.03); }
.com-icon { width: 36px; height: 36px; border-radius: 10px; display: flex; align-items: center; justify-content: center; font-size: 16px; flex-shrink: 0; }
.com-icon.recordatorio { background: rgba(0,212,255,0.12); }
.com-icon.aviso  { background: rgba(168,85,247,0.12); }
.com-icon.examen { background: rgba(239,68,68,0.12); }
.com-icon.tarea  { background: rgba(255,215,0,0.12); }
.com-info { flex: 1; min-width: 0; }
.com-info strong { display: block; font-size: 13px; font-weight: 600; margin-bottom: 3px; }
.com-dest { font-size: 11px; color: #7a96b0; display: block; margin-bottom: 4px; }
.com-preview { font-size: 12px; color: #7a96b0; line-height: 1.5; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.com-meta { display: flex; flex-direction: column; align-items: flex-end; gap: 6px; flex-shrink: 0; }
.com-enviados { font-size: 11px; color: #7a96b0; white-space: nowrap; }
.badge-tipo { font-size: 10px; font-weight: 600; padding: 3px 8px; border-radius: 100px; text-transform: capitalize; }
.badge-tipo.recordatorio { background: rgba(0,212,255,0.12); color: #00d4ff; }
.badge-tipo.aviso  { background: rgba(168,85,247,0.12); color: #a855f7; }
.badge-tipo.examen { background: rgba(239,68,68,0.12);  color: #f87171; }
.badge-tipo.tarea  { background: rgba(255,215,0,0.12);  color: #ffd700; }

/* Modal */
.modal-overlay { position: fixed; inset: 0; background: rgba(0,0,0,0.75); backdrop-filter: blur(6px); display: flex; align-items: center; justify-content: center; z-index: 100; }
.modal { background: #0a1628; border: 1px solid rgba(0,212,255,0.15); border-radius: 20px; width: 500px; overflow: hidden; }
.modal-header { display: flex; justify-content: space-between; align-items: center; padding: 20px 24px; border-bottom: 1px solid rgba(0,212,255,0.08); }
.modal-header h2 { font-size: 16px; font-weight: 600; }
.btn-cerrar-modal { background: transparent; border: none; color: #7a96b0; font-size: 16px; cursor: pointer; padding: 4px; }
.btn-cerrar-modal:hover { color: #f0f8ff; }

.email-preview { margin: 20px 24px; background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.07); border-radius: 12px; overflow: hidden; }
.email-header { display: flex; justify-content: space-between; align-items: center; padding: 14px 18px; background: linear-gradient(135deg, #0077b6, #00b4d8); }
.email-logo { font-size: 12px; font-weight: 700; letter-spacing: 2px; color: white; }
.email-badge { font-size: 11px; font-weight: 600; background: rgba(255,255,255,0.2); padding: 4px 10px; border-radius: 100px; color: white; }
.email-body { padding: 20px 18px; }
.email-body h3 { font-size: 16px; font-weight: 700; margin-bottom: 12px; }
.email-body p { font-size: 13px; color: #7a96b0; line-height: 1.7; }
.email-footer { padding: 12px 18px; border-top: 1px solid rgba(255,255,255,0.05); font-size: 11px; color: #7a96b0; }

.modal-btns { display: flex; gap: 12px; padding: 16px 24px; border-top: 1px solid rgba(0,212,255,0.08); }
.btn-cancelar { flex: 1; padding: 11px; background: transparent; border: 1px solid rgba(255,255,255,0.08); border-radius: 10px; color: #7a96b0; font-family: 'Sora', sans-serif; font-size: 13px; cursor: pointer; }
.btn-confirmar { flex: 2; padding: 11px; background: linear-gradient(135deg, #0077b6, #00b4d8); border: none; border-radius: 10px; color: white; font-family: 'Sora', sans-serif; font-size: 13px; font-weight: 600; cursor: pointer; }
.btn-confirmar:hover { box-shadow: 0 6px 20px rgba(0,180,216,0.35); }
</style>