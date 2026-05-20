from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional, List
from datetime import date, datetime

# =============================================================================
# 🔹 CLASES BASE (ya existentes - NO borrar)
# =============================================================================

class LoginRequest(BaseModel):
    """Request para login con email/password"""
    correo_electronico: EmailStr
    password: str

class Token(BaseModel):
    """Respuesta de token JWT"""
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    """Datos internos del payload del token"""
    user_id: Optional[int] = None
    username: Optional[str] = None  # email o CI
    roles: Optional[List[str]] = None

class ChangePasswordRequest(BaseModel):
    """Para cambiar contraseña (requiere la actual)"""
    current_password: str = Field(..., min_length=8)
    new_password: str = Field(..., min_length=8)
    
    @field_validator('new_password')
    def password_strength(cls, v):
        if not any(c.isupper() for c in v) or not any(c.isdigit() for c in v):
            raise ValueError('La contraseña debe incluir mayúscula y número')
        return v

# =============================================================================
# 🔹 NUEVAS CLASES PARA FLUJO DE EMAIL Y REGISTRO POR ROL
# =============================================================================

class StudentRegisterRequest(BaseModel):
    """Registro público para ESTUDIANTE"""
    ci: str = Field(..., min_length=5, max_length=20)
    correo_electronico: EmailStr
    password: str = Field(..., min_length=8)
    nombre: str = Field(..., max_length=50)
    ape_paterno: str = Field(..., max_length=50)
    ape_materno: str = Field(..., max_length=50)
    celular: Optional[str] = Field(None, max_length=20)
    fecha_nacimiento: Optional[date] = None
    direccion: Optional[str] = None
    sexo: Optional[str] = Field(None, max_length=10)
    # Campos de ESTUDIANTE (opcionales, se guardan NULL si no se envían)
    institucion: Optional[str] = Field(None, max_length=255)
    fecha_ingreso: Optional[date] = None

    @field_validator('ci')
    def ci_must_be_numeric(cls, v):
        if not v.isdigit():
            raise ValueError('La CI solo debe contener números')
        return v
    
    @field_validator('password')
    def password_strength_register(cls, v):
        if not any(c.isupper() for c in v) or not any(c.isdigit() for c in v):
            raise ValueError('La contraseña debe incluir mayúscula y número')
        return v

class TeacherCreateRequest(BaseModel):
    """Creación de DOCENTE (solo ADMIN/SUPERADMIN)"""
    ci: str = Field(..., min_length=5, max_length=20)
    correo_electronico: EmailStr
    password: str = Field(..., min_length=8)
    nombre: str = Field(..., max_length=50)
    ape_paterno: str = Field(..., max_length=50)
    ape_materno: str = Field(..., max_length=50)
    celular: Optional[str] = Field(None, max_length=20)
    fecha_nacimiento: Optional[date] = None
    # Campos obligatorios de DOCENTE
    especialidad: str = Field(..., max_length=100)
    grado_academico: str = Field(..., max_length=100)
    anios_experiencia: int = Field(..., ge=0)
    # Campos opcionales de PORTAFOLIO
    linkedin: Optional[str] = Field(None, max_length=255)
    github: Optional[str] = Field(None, max_length=255)
    direccion_cv: Optional[str] = Field(None, max_length=500)

class AdminCreateRequest(BaseModel):
    """Creación de ADMIN (solo SUPERADMIN)"""
    ci: str = Field(..., min_length=5, max_length=20)
    correo_electronico: EmailStr
    password: str = Field(..., min_length=8)
    nombre: str = Field(..., max_length=50)
    ape_paterno: str = Field(..., max_length=50)
    ape_materno: str = Field(..., max_length=50)
    celular: Optional[str] = Field(None, max_length=20)
    fecha_nacimiento: Optional[date] = None

# =============================================================================
# 🔹 CLASES PARA VERIFICACIÓN DE EMAIL Y RECUPERACIÓN
# =============================================================================

class EmailVerificationResponse(BaseModel):
    """Respuesta tras verificar email"""
    message: str

class PasswordResetRequest(BaseModel):
    """Solicitud de recuperación de contraseña"""
    correo_electronico: EmailStr

class PasswordResetConfirm(BaseModel):
    """Confirmación de reset con nueva contraseña"""
    token: str
    nueva_password: str = Field(..., min_length=8)
    
    @field_validator('nueva_password')
    def password_strength_reset(cls, v):
        if not any(c.isupper() for c in v) or not any(c.isdigit() for c in v):
            raise ValueError('Debe incluir mayúscula y número')
        return v

class RoleInfo(BaseModel):
    """Información del rol del usuario"""
    id_rol: int
    nombre: str
    descripcion: Optional[str] = None
    
    class Config:
        from_attributes = True

class InstanceInfo(BaseModel):
    """Información de la instancia (usuario-rol)"""
    id_usuario: int
    id_rol: int
    fecha_asignacion: Optional[datetime] = None
    rol: Optional[RoleInfo] = None
    
    class Config:
        from_attributes = True

class UserInfo(BaseModel):
    """Datos públicos del usuario (sin password)"""
    id_usuario: int
    ci: Optional[str]
    correo_electronico: str
    nombre: str
    ape_paterno: Optional[str]
    ape_materno: Optional[str]
    celular: Optional[str]
    foto_perfil: Optional[str]
    estado: str
    fecha_registro: datetime
    created_at: datetime
    updated_at: datetime
    instancias: Optional[List[InstanceInfo]] = []
    
    class Config:
        from_attributes = True

class LoginResponse(BaseModel):
    """Respuesta completa de login: token + usuario + rol principal"""
    access_token: str
    token_type: str
    usuario: UserInfo
    rol_principal: Optional[str] = None  # Rol con mayor privilegio o primero asignado
    mensaje: Optional[str] = "Login exitoso"