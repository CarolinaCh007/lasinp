from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import Optional, Dict, Any
from datetime import datetime

from app.modules.auth.models.usuario import Usuario
from app.modules.auth.models.instancia import Instancia
from app.modules.auth.models.rol import Rol
from app.modules.auth.services.auth_service import (
    hashear_password, 
    registrar_auditoria,
    crear_token_verificacion_email,
    crear_token_reset_password,
    verificar_token_seguro
)
from app.shared.email import EmailService

# =============================================================================
# 🔹 FUNCIONES DE CONSULTA DE USUARIOS (Solo tablas de auth/)
# =============================================================================

def obtener_usuario_por_email(db: Session, email: str) -> Optional[Usuario]:
    """Busca un usuario por su correo electrónico"""
    return db.execute(
        select(Usuario).where(Usuario.correo_electronico == email)
    ).scalar_one_or_none()

def obtener_usuario_por_ci(db: Session, ci: str) -> Optional[Usuario]:
    """Busca un usuario por su cédula de identidad"""
    return db.execute(
        select(Usuario).where(Usuario.ci == ci)
    ).scalar_one_or_none()

def obtener_usuario_por_id(db: Session, user_id: int) -> Optional[Usuario]:
    """Busca un usuario por su ID"""
    return db.get(Usuario, user_id)

def obtener_roles_de_usuario(db: Session, id_usuario: int) -> list[str]:
    """Obtiene la lista de nombres de rol que tiene un usuario"""
    query = select(Rol.nombre).join(Instancia).where(Instancia.id_usuario == id_usuario)
    return db.execute(query).scalars().all()

# =============================================================================
# 🔹 FUNCIÓN PRINCIPAL: CREAR USUARIO CON ROL (Solo auth/)
# =============================================================================

def crear_usuario_con_rol(
    db: Session,
    usuario_data: Dict[str, Any],
    id_rol: int
) -> Usuario:
    """
    Crea usuario + instancia en transacción atómica.
    
    - estado inicial: 'pendiente'
    - envía email de verificación
    - registra auditoría
    
    ⚠️ NO crea Estudiante/Docente/Portafolio (eso lo hace academic/)
    """
    try:
        # 1. Hashear contraseña y forzar estado inicial
        usuario_data["password"] = hashear_password(usuario_data["password"])
        usuario_data["estado"] = "pendiente"
        
        # 2. Crear USUARIO
        db_usuario = Usuario(**usuario_data)
        db.add(db_usuario)
        db.flush()  # Obtiene id_usuario generado sin hacer commit aún
        
        # 3. Crear INSTANCIA (relación usuario-rol)
        instancia = Instancia(id_usuario=db_usuario.id_usuario, id_rol=id_rol)
        db.add(instancia)
        
        # 4. Commit de la transacción de auth/
        db.commit()
        db.refresh(db_usuario)
        
        # 5. Generar token de verificación y enviar email
        token = crear_token_verificacion_email({
            "sub": str(db_usuario.id_usuario), 
            "email": db_usuario.correo_electronico
        })
        EmailService.send_verification_email(
            to_email=db_usuario.correo_electronico,
            username=db_usuario.nombre,
            token=token
        )
        
        # 6. Registrar auditoría
        registrar_auditoria(db, db_usuario.id_usuario, "CREATE_USER", "usuario")
        
        return db_usuario
        
    except Exception as e:
        db.rollback()
        raise e

# =============================================================================
# 🔹 FUNCIONES DE VERIFICACIÓN DE EMAIL
# =============================================================================

def verificar_email_usuario(db: Session, token: str) -> Optional[Usuario]:
    """
    Verifica token de email y activa la cuenta.
    
    Returns:
        Usuario activado si el token es válido, None si no.
    """
    payload = verificar_token_seguro(token, "email_verification")
    if not payload:
        return None
    
    user_id = payload.get("sub")
    email = payload.get("email")
    
    if not user_id or not email:
        return None
    
    usuario = db.get(Usuario, int(user_id))
    if not usuario or usuario.correo_electronico != email:
        return None
    
    # ✅ Activar cuenta: pendiente → activo
    usuario.estado = "activo"
    db.commit()
    db.refresh(usuario)
    
    registrar_auditoria(db, usuario.id_usuario, "EMAIL_VERIFIED", "usuario")
    return usuario

# =============================================================================
# 🔹 FUNCIONES DE RECUPERACIÓN DE CONTRASEÑA
# =============================================================================

def solicitar_reset_password(db: Session, correo_electronico: str, request_ip: Optional[str] = None) -> bool:
    """
    Solicita reset de contraseña: genera token y envía email.
    
    Returns:
        True si el email existe (y se envió correo), False si no.
    """
    usuario = obtener_usuario_por_email(db, correo_electronico)
    
    if not usuario:
        registrar_auditoria(db, None, "PASSWORD_RESET_REQUESTED", "usuario", request_ip)
        return False
    
    token = crear_token_reset_password({
        "sub": str(usuario.id_usuario), 
        "email": usuario.correo_electronico
    })
    
    EmailService.send_password_reset_email(
        to_email=usuario.correo_electronico,
        username=usuario.nombre,
        token=token
    )
    
    registrar_auditoria(db, usuario.id_usuario, "PASSWORD_RESET_SENT", "usuario", request_ip)
    return True

def resetear_contrasena(db: Session, token: str, nueva_password: str) -> Optional[Usuario]:
    """
    Resetea contraseña con token válido.
    
    Returns:
        Usuario con contraseña actualizada si el token es válido, None si no.
    """
    payload = verificar_token_seguro(token, "password_reset")
    if not payload:
        return None
    
    user_id = payload.get("sub")
    email = payload.get("email")
    
    if not user_id or not email:
        return None
    
    usuario = db.get(Usuario, int(user_id))
    # Validar: existe + email coincide + cuenta está activa
    if not usuario or usuario.correo_electronico != email or usuario.estado != "activo":
        return None
    
    usuario.password = hashear_password(nueva_password)
    db.commit()
    db.refresh(usuario)
    
    registrar_auditoria(db, usuario.id_usuario, "PASSWORD_RESET_COMPLETED", "usuario")
    return usuario

# =============================================================================
# 🔹 FUNCIONES DE ACTUALIZACIÓN DE USUARIO
# =============================================================================

def actualizar_usuario(db: Session, id_usuario: int, update_data: Dict[str, Any]) -> Optional[Usuario]:
    """
    Actualiza datos de un usuario existente.
    
    Returns:
        Usuario actualizado o None si no existe.
    """
    db_usuario = db.get(Usuario, id_usuario)
    if not db_usuario:
        return None
    
    # Si viene password en los datos, hashearlo primero
    if "password" in update_data and update_data["password"]:
        update_data["password"] = hashear_password(update_data["password"])
    
    # Actualizar solo campos que no son None y existen en el modelo
    for key, value in update_data.items():
        if value is not None and hasattr(db_usuario, key):
            setattr(db_usuario, key, value)
    
    # Actualizar timestamp de actualización
    db_usuario.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(db_usuario)
    
    registrar_auditoria(db, db_usuario.id_usuario, "UPDATE_USER", "usuario")
    return db_usuario