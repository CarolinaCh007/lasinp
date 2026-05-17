import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional
from app.core.config import settings

class EmailService:
    """Servicio para envío de emails (SMTP o servicio externo)"""
    
    @staticmethod
    def send_verification_email(to_email: str, username: str, token: str):
        """Envía email de verificación de cuenta"""
        # En producción, usar variable de entorno para el frontend URL
        frontend_url = getattr(settings, "FRONTEND_URL", "http://localhost:3000")
        verify_link = f"{frontend_url}/verify-email?token={token}"
        
        subject = "✅ Verifica tu cuenta - Sistema Educativo"
        body = f"""
        Hola {username},

        Gracias por registrarte en nuestro sistema educativo.

        Para activar tu cuenta, por favor haz clic en el siguiente enlace:
        {verify_link}

        Este enlace expira en 24 horas.

        Si no solicitaste este registro, ignora este mensaje.

        Saludos,
        Equipo UMSA
        """
        
        EmailService._send_email(to_email, subject, body)
    
    @staticmethod
    def send_password_reset_email(to_email: str, username: str, token: str):
        """Envía email para restablecer contraseña"""
        frontend_url = getattr(settings, "FRONTEND_URL", "http://localhost:3000")
        reset_link = f"{frontend_url}/reset-password?token={token}"
        
        subject = "🔑 Restablece tu contraseña"
        body = f"""
        Hola {username},

        Hemos recibido una solicitud para restablecer tu contraseña.

        Para crear una nueva contraseña, haz clic aquí:
        {reset_link}

        Este enlace expira en 1 hora por seguridad.

        Si no solicitaste este cambio, ignora este mensaje o contacta a soporte.

        Saludos,
        Equipo UMSA
        """
        
        EmailService._send_email(to_email, subject, body)
    
    @staticmethod
    def _send_email(to_email: str, subject: str, body: str):
        """Método interno para enviar email vía SMTP"""
        # 🔹 Configuración desde variables de entorno
        smtp_server = getattr(settings, "SMTP_SERVER", "smtp.gmail.com")
        smtp_port = getattr(settings, "SMTP_PORT", 587)
        smtp_user = getattr(settings, "SMTP_USER", "olujann@fcpn.edu.bo")
        smtp_password = getattr(settings, "SMTP_PASSWORD", "morp mhha yygm auld")
        from_email = getattr(settings, "FROM_EMAIL", smtp_user)
        
        # Si no hay credenciales SMTP, solo loguear (para desarrollo)
        if not smtp_user or not smtp_password:
            print(f"📧 [DEV MODE] Email a {to_email}: {subject}")
            print(f"🔗 Link: {body.split('http')[1].split()[0] if 'http' in body else 'N/A'}")
            return
        
        # Crear mensaje
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = from_email
        msg["To"] = to_email
        
        # Versión HTML (opcional pero recomendado)
        html = f"""
        <html>
          <body>
            <h2>{subject}</h2>
            <p>{body.replace(chr(10), '<br>')}</p>
          </body>
        </html>
        """
        
        msg.attach(MIMEText(body, "plain"))
        msg.attach(MIMEText(html, "html"))
        
        # Enviar
        try:
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(smtp_user, smtp_password)
                server.sendmail(from_email, [to_email], msg.as_string())
            print(f"✅ Email enviado a {to_email}")
        except Exception as e:
            print(f"❌ Error enviando email: {e}")
            # En producción, considerar reintentos o cola de emails