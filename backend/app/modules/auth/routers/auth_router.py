from fastapi import APIRouter, Depends, HTTPException, status, Request, Query
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta, datetime
from typing import Optional


from app.core.database import get_db
from app.core.config import settings
from app.modules.auth.schemas.usuario import UsuarioCreate, UsuarioRead
from app.modules.auth.schemas.auth import (
    Token, 
    ChangePasswordRequest,
    StudentRegisterRequest,
    TeacherCreateRequest,
    AdminCreateRequest,
    EmailVerificationResponse,
    PasswordResetRequest,
    PasswordResetConfirm,
    LoginResponse

)
from app.modules.auth.services.auth_service import (
    hashear_password, 
    crear_token_acceso, 
    verificar_password,
    registrar_auditoria, 
    cambiar_password
)
from app.modules.auth.services.usuario_service import (
    obtener_usuario_por_email, 
    crear_usuario_con_rol,
    verificar_email_usuario,
    solicitar_reset_password,
    resetear_contrasena,
        obtener_usuario_completo_con_roles
)
from app.core.security import get_current_user, require_role
from app.modules.auth.models.usuario import Usuario

router = APIRouter(prefix="/auth", tags=["🔐 Autenticación"])

# =============================================================================
# 🔹 ENDPOINTS DE AUTENTICACIÓN BÁSICA
# =============================================================================

@router.post("/login", response_model=LoginResponse)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
    request: Request = None
):
    """
    Login completo: devuelve token + datos del usuario + rol principal.
    
    Request (form-urlencoded):
    - username: correo electrónico
    - password: contraseña
    
    Response:
    - access_token: JWT para autenticación
    - usuario: datos públicos del usuario
    - rol_principal: rol con mayor privilegio (para RBAC en frontend)
    """
    # 1. Buscar usuario por email (username en OAuth2Form)
    usuario = obtener_usuario_por_email(db, form_data.username)
    
    if not usuario or not verificar_password(form_data.password, usuario.password):
        ip = request.client.host if request else None
        registrar_auditoria(db, None, "LOGIN_FAILED", "usuario", ip)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 2. Verificar que la cuenta esté activa
    if usuario.estado != "activo":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cuenta no verificada. Estado actual: {usuario.estado}"
        )
    
    # 3. Generar token JWT
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = crear_token_acceso(
        data={"sub": str(usuario.id_usuario)},
        expires_delta=access_token_expires
    )
    
    # 4. Obtener usuario completo con roles (nueva función)
    usuario_completo = obtener_usuario_completo_con_roles(db, usuario.id_usuario)
    
    if not usuario_completo:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al obtener datos completos del usuario"
        )
    
    # 5. Registrar auditoría de login exitoso
    ip = request.client.host if request else None
    registrar_auditoria(db, usuario.id_usuario, "LOGIN_SUCCESS", "usuario", ip)
    
    # 6. Retornar respuesta completa
    return LoginResponse(
        access_token=access_token,
        token_type="bearer",
        usuario=usuario_completo,
        rol_principal=usuario_completo["rol_principal"],
        mensaje="Login exitoso"
    )

@router.get("/me", response_model=UsuarioRead)
def leer_usuario_actual(
    current_user: Usuario = Depends(get_current_user)
):
    """Obtener información del usuario autenticado."""
    return current_user

@router.post("/logout", status_code=status.HTTP_200_OK)
def logout(
    request: Request,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Logout profesional: registra acción y delega limpieza al cliente."""
    ip = request.client.host if request else None
    registrar_auditoria(db, current_user.id_usuario, "LOGOUT", "usuario", ip)
    return {"message": "Sesión cerrada. Elimine el token del almacenamiento local."}

@router.put("/change-password", status_code=status.HTTP_200_OK)
def cambiar_contrasena(
    password_data: ChangePasswordRequest,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Cambiar contraseña del usuario autenticado"""
    if not cambiar_password(db, current_user, password_data.current_password, password_data.new_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Contraseña actual incorrecta"
        )
    return {"message": "Contraseña actualizada correctamente"}

# =============================================================================
# 🔹 ENDPOINTS DE REGISTRO POR ROL (Solo Usuario + Instancia)
# =============================================================================

@router.post("/register/student", response_model=UsuarioRead, status_code=status.HTTP_201_CREATED)
def registrar_estudiante_publico(
    student_data: StudentRegisterRequest,
    db: Session = Depends(get_db),
    request: Request = None
):
    """
    Registro público para estudiantes.
    Crea: USUARIO(estado='pendiente') + INSTANCIA(rol=4)
    ⚠️ El perfil académico (institucion, fecha_ingreso) se completa después vía /academic/estudiantes/
    """
    if obtener_usuario_por_email(db, student_data.correo_electronico):
        raise HTTPException(status_code=400, detail="Correo ya registrado")
    
    # Solo datos de USUARIO (excluir campos académicos)
    usuario_data = student_data.model_dump(exclude={"institucion", "fecha_ingreso"})
    
    # Crear solo Usuario + Instancia (rol=4 = ESTUDIANTE)
    nuevo_usuario = crear_usuario_con_rol(
        db=db,
        usuario_data=usuario_data,
        id_rol=4
    )
    
    ip = request.client.host if request else None
    registrar_auditoria(db, nuevo_usuario.id_usuario, "REGISTER_STUDENT", "usuario", ip)
    
    return nuevo_usuario

@router.post("/users/teacher", response_model=UsuarioRead, status_code=status.HTTP_201_CREATED)
def crear_docente_admin(
    teacher_data: TeacherCreateRequest,
    db: Session = Depends(get_db),
    request: Request = None,
    current_user: Usuario = Depends(require_role("superadmin"))
):
    """
    Crear docente (solo para administradores).
    Crea: USUARIO + INSTANCIA(rol=3)
    ⚠️ El perfil profesional (especialidad, portafolio) se completa después vía /academic/docentes/
    """
    if obtener_usuario_por_email(db, teacher_data.correo_electronico):
        raise HTTPException(status_code=400, detail="Correo ya registrado")
    
    # Solo datos de USUARIO (excluir campos profesionales)
    usuario_data = teacher_data.model_dump(exclude={
        "especialidad", "grado_academico", "anios_experiencia",
        "linkedin", "github", "direccion_cv"
    })
    
    # Crear solo Usuario + Instancia (rol=3 = DOCENTE)
    nuevo_usuario = crear_usuario_con_rol(
        db=db,
        usuario_data=usuario_data,
        id_rol=3
    )
    
    ip = request.client.host if request else None
    registrar_auditoria(db, nuevo_usuario.id_usuario, "CREATE_TEACHER", "usuario", ip)
    
    return nuevo_usuario

@router.post("/users/admin", response_model=UsuarioRead, status_code=status.HTTP_201_CREATED)
def crear_admin(
    admin_data: AdminCreateRequest,
    db: Session = Depends(get_db),
    request: Request = None,
    current_user: Usuario = Depends(require_role("superadmin"))
):
    """Crear administrador (solo superadmin)"""
    if obtener_usuario_por_email(db, admin_data.correo_electronico):
        raise HTTPException(status_code=400, detail="Correo ya registrado")
    
    usuario_data = admin_data.model_dump()
    
    nuevo_usuario = crear_usuario_con_rol(
        db=db,
        usuario_data=usuario_data,
        id_rol=2  # ADMIN
    )
    
    ip = request.client.host if request else None
    registrar_auditoria(db, nuevo_usuario.id_usuario, "CREATE_ADMIN", "usuario", ip)
    
    return nuevo_usuario

# =============================================================================
# 🔹 ENDPOINTS DE VERIFICACIÓN Y RECUPERACIÓN
# =============================================================================

@router.get("/verify-email", response_model=EmailVerificationResponse)
def verificar_email(
    token: str = Query(..., description="Token de verificación"),
    db: Session = Depends(get_db)
):
    """Verifica token de email y activa la cuenta (pendiente → activo)."""
    usuario = verificar_email_usuario(db, token)
    
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Token inválido o expirado. Solicita un nuevo correo de verificación."
        )
    
    return {"message": "✅ Cuenta verificada exitosamente. Ahora puedes iniciar sesión."}

@router.post("/forgot-password", status_code=status.HTTP_200_OK)
def solicitar_recuperacion(
    request_data: PasswordResetRequest,
    db: Session = Depends(get_db),
    request: Request = None
):
    """Solicita recuperación de contraseña."""
    ip = request.client.host if request else None
    solicitar_reset_password(db, request_data.correo_electronico, ip)
    
    return {"message": "Si el correo está registrado, recibirás instrucciones para restablecer tu contraseña."}

@router.post("/reset-password", status_code=status.HTTP_200_OK)
def confirmar_reset_password(
    request_data: PasswordResetConfirm,
    db: Session = Depends(get_db)
):
    """Confirma el reset de contraseña con token válido."""
    usuario = resetear_contrasena(db, request_data.token, request_data.nueva_password)
    
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Token inválido, expirado o cuenta no verificada."
        )
    
    return {"message": "✅ Contraseña actualizada exitosamente. Ahora puedes iniciar sesión."}

@router.post("/resend-verification", status_code=status.HTTP_200_OK)
def reenviar_verificacion(
    request_data: PasswordResetRequest,
    db: Session = Depends(get_db),
    request: Request = None
):
    """Reenvía email de verificación si el usuario aún está 'pendiente'"""
    usuario = obtener_usuario_por_email(db, request_data.correo_electronico)
    
    if not usuario:
        return {"message": "Si el correo está registrado, se enviará un nuevo enlace de verificación."}
    
    if usuario.estado == "activo":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Esta cuenta ya está verificada. Puedes iniciar sesión."
        )
    
    from app.modules.auth.services.auth_service import crear_token_verificacion_email
    from app.shared.email import EmailService
    
    token = crear_token_verificacion_email({
        "sub": str(usuario.id_usuario), 
        "email": usuario.correo_electronico
    })
    EmailService.send_verification_email(usuario.correo_electronico, usuario.nombre, token)
    
    ip = request.client.host if request else None
    registrar_auditoria(db, usuario.id_usuario, "VERIFICATION_RESENT", "usuario", ip)
    
    return {"message": "Nuevo enlace de verificación enviado."}