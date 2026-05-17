from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional
from datetime import date, datetime

# =============================================================================
# 🔹 SCHEMAS PARA CREAR/ACTUALIZAR USUARIO
# =============================================================================

class UsuarioCreate(BaseModel):
    """Datos requeridos para crear un usuario (registro)"""
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
    foto_perfil: Optional[str] = None
    # Para registro público, el frontend puede enviar id_rol
    id_rol: Optional[int] = None

    @field_validator('ci')
    def ci_must_be_numeric(cls, v):
        if not v.isdigit():
            raise ValueError('La CI solo debe contener números')
        return v

    @field_validator('password')
    def password_strength(cls, v):
        if not any(c.isupper() for c in v) or not any(c.isdigit() for c in v):
            raise ValueError('La contraseña debe incluir mayúscula y número')
        return v

class UsuarioUpdate(BaseModel):
    """Datos opcionales para actualizar un usuario"""
    ci: Optional[str] = Field(None, min_length=5, max_length=20)
    correo_electronico: Optional[EmailStr] = None
    nombre: Optional[str] = Field(None, max_length=50)
    ape_paterno: Optional[str] = Field(None, max_length=50)
    ape_materno: Optional[str] = Field(None, max_length=50)
    celular: Optional[str] = Field(None, max_length=20)
    fecha_nacimiento: Optional[date] = None
    direccion: Optional[str] = None
    sexo: Optional[str] = Field(None, max_length=10)
    foto_perfil: Optional[str] = None
    estado: Optional[str] = Field(None, pattern="^(pendiente|activo|inactivo)$")

    @field_validator('ci')
    def ci_must_be_numeric_if_present(cls, v):
        if v is not None and not v.isdigit():
            raise ValueError('La CI solo debe contener números')
        return v

# =============================================================================
# 🔹 SCHEMAS PARA RESPUESTAS DE API (READ)
# =============================================================================

class UsuarioRead(BaseModel):
    """
    Respuesta de API: datos públicos de un usuario.
    ✅ estado es STRING, no booleano (coherente con la BD)
    """
    id_usuario: int
    ci: str
    correo_electronico: str
    nombre: str
    ape_paterno: str
    ape_materno: str
    celular: Optional[str]
    fecha_nacimiento: Optional[date]
    direccion: Optional[str]
    sexo: Optional[str]
    foto_perfil: Optional[str]
    # ✅ CORRECCIÓN CLAVE: estado es string, no bool
    estado: str  # 'pendiente', 'activo', 'inactivo'
    fecha_registro: Optional[datetime]
    ultimo_acceso: Optional[datetime]

    class Config:
        from_attributes = True  # Vital para que SQLAlchemy funcione con Pydantic v2

class UsuarioPublic(BaseModel):
    """Datos mínimos para mostrar en listados públicos (sin información sensible)"""
    id_usuario: int
    nombre: str
    ape_paterno: str
    foto_perfil: Optional[str]
    estado: str

    class Config:
        from_attributes = True