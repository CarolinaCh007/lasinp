from pydantic import BaseModel, Field, EmailStr, field_validator
from typing import Optional
from datetime import date, datetime

class UsuarioCreate(BaseModel):
    ci: Optional[str] = Field(None, max_length=20)
    correo_electronico: EmailStr
    password: str = Field(..., min_length=8)
    nombre: str = Field(..., max_length=50)
    ape_paterno: Optional[str] = Field(None, max_length=50)
    ape_materno: Optional[str] = Field(None, max_length=50)
    celular: Optional[str] = Field(None, max_length=20)
    fecha_nacimiento: Optional[date] = None
    direccion: Optional[str] = None
    sexo: Optional[str] = Field(None, pattern="^(M|F|Otro)$")
    foto_perfil: Optional[str] = None
    estado: Optional[str] = Field("pendiente", pattern="^(activo|inactivo|pendiente|bloqueado)$")

class UsuarioRead(BaseModel):
    id_usuario: int
    ci: Optional[str]
    correo_electronico: str
    nombre: str
    ape_paterno: Optional[str]
    ape_materno: Optional[str]
    celular: Optional[str]
    fecha_nacimiento: Optional[date]
    direccion: Optional[str]
    sexo: Optional[str]
    foto_perfil: Optional[str]
    estado: str
    fecha_registro: datetime
    created_at: datetime
    updated_at: datetime
    # ❌ ultimo_acceso ELIMINADO

    class Config:
        from_attributes = True

class UsuarioUpdate(BaseModel):
    ci: Optional[str] = Field(None, max_length=20)
    correo_electronico: Optional[EmailStr] = None
    nombre: Optional[str] = Field(None, max_length=50)
    ape_paterno: Optional[str] = Field(None, max_length=50)
    ape_materno: Optional[str] = Field(None, max_length=50)
    celular: Optional[str] = Field(None, max_length=20)
    fecha_nacimiento: Optional[date] = None
    direccion: Optional[str] = None
    sexo: Optional[str] = Field(None, pattern="^(M|F|Otro)$")
    foto_perfil: Optional[str] = None
    estado: Optional[str] = Field(None, pattern="^(activo|inactivo|pendiente|bloqueado)$")

from pydantic import BaseModel, Field

class RolRead(BaseModel):
    id_rol: int; nombre: str; descripcion: Optional[str]
    class Config: from_attributes = True

class AsignarRolRequest(BaseModel):
    nombre_rol: str = Field(..., max_length=50, description="Nombre exacto del rol en BD (ej: ADMIN, DOCENTE)")

class EstadoUpdateRequest(BaseModel):
    estado: str = Field(..., pattern="^(activo|inactivo|pendiente|bloqueado)$")