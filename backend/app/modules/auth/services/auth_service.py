from datetime import datetime, timedelta
from typing import Optional
from jose import jwt, JWTError
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.core.config import settings
from app.modules.auth.models.log_auditoria import LogAuditoria
from app.shared.email import EmailService

# 🔐 Configuración de hashing (bcrypt)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# =============================================================================
# 🔹 FUNCIONES DE CONTRASEÑA
# =============================================================================

def verificar_password(password_plano: str, password_hash: str) -> bool:
    """Compara contraseña en texto plano con hash almacenado"""
    return pwd_context.verify(password_plano, password_hash)

def hashear_password(password: str) -> str:
    """Convierte contraseña en hash seguro con bcrypt"""
    return pwd_context.hash(password)

# =============================================================================
# 🔹 FUNCIONES DE TOKENS JWT
# =============================================================================

def crear_token_acceso(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Genera token JWT para autenticación de API (15-30 min)"""
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def crear_token_verificacion_email(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Genera token para verificación de email (24 horas)"""
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(hours=24))
    to_encode.update({"exp": expire, "type": "email_verification"})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def crear_token_reset_password(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Genera token para recuperación de contraseña (1 hora)"""
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(hours=1))
    to_encode.update({"exp": expire, "type": "password_reset"})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def verificar_token_seguro(token: str, expected_type: str) -> Optional[dict]:
    """Verifica token de email o password reset"""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        token_type = payload.get("type")
        
        if token_type != expected_type:
            return None
        
        exp_timestamp = payload.get("exp")
        if exp_timestamp and datetime.utcnow() > datetime.fromtimestamp(exp_timestamp):
            return None
            
        return payload
    except JWTError:
        return None

# =============================================================================
# 🔹 FUNCIONES DE AUDITORÍA
# =============================================================================

def registrar_auditoria(
    db: Session, 
    id_usuario: Optional[int], 
    accion: str, 
    tabla_afectada: Optional[str] = None, 
    ip: Optional[str] = None
):
    """Registra acción en LOG_AUDITORIA"""
    log = LogAuditoria(
        id_usuario=id_usuario,
        accion=accion,
        tabla_afectada=tabla_afectada,
        direccion_ip=ip
    )
    db.add(log)
    db.commit()

# =============================================================================
# 🔹 FUNCIONES DE GESTIÓN DE CONTRASEÑA
# =============================================================================

def cambiar_password(db: Session, usuario, current_password: str, new_password: str) -> bool:
    """Cambia la contraseña de un usuario verificando la actual"""
    if not verificar_password(current_password, usuario.password):
        return False
    
    usuario.password = hashear_password(new_password)
    db.commit()
    
    registrar_auditoria(db, usuario.id_usuario, "CHANGE_PASSWORD", "usuario")
    
    return True