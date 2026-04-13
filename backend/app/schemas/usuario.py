from pydantic import BaseModel, EmailStr
from datetime import date, datetime
from typing import Optional

class RolBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None

class RolResponse(RolBase):
    id_rol: int
    class Config:
        from_attributes = True

class UsuarioCreate(BaseModel):
    ci: Optional[str] = None
    correo_electronico: EmailStr
    password: str
    nombre: str
    ape_paterno: Optional[str] = None
    ape_materno: Optional[str] = None
    celular: Optional[str] = None
    fecha_nacimiento: Optional[date] = None
    direccion: Optional[str] = None
    sexo: Optional[str] = None

class UsuarioResponse(BaseModel):
    id_usuario: int
    ci: Optional[str] = None
    correo_electronico: str
    nombre: str
    ape_paterno: Optional[str] = None
    ape_materno: Optional[str] = None
    celular: Optional[str] = None
    estado: Optional[str] = None
    fecha_registro: Optional[datetime] = None
    foto_perfil: Optional[str] = None

    class Config:
        from_attributes = True

class UsuarioUpdate(BaseModel):
    nombre: Optional[str] = None
    ape_paterno: Optional[str] = None
    ape_materno: Optional[str] = None
    celular: Optional[str] = None
    direccion: Optional[str] = None
    foto_perfil: Optional[str] = None

class LoginRequest(BaseModel):
    correo_electronico: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    usuario: UsuarioResponse
    rol: str


    