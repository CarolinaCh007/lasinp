from pydantic import BaseModel, Field, field_validator  # ← Importar field_validator
from typing import Optional
from datetime import date, datetime

class DocenteCreate(BaseModel):
    id_usuario: int = Field(..., gt=0, description="ID del usuario base")
    especialidad: Optional[str] = Field(None, max_length=100)
    grado_academico: Optional[str] = Field(None, max_length=100)
    anios_experiencia: Optional[int] = Field(None, ge=0)  # ge=0 → greater or equal
    fecha_inicio: Optional[date] = None
    estado: Optional[str] = Field(None, pattern="^(activo|inactivo)$")

    @field_validator('id_usuario')
    @classmethod
    def validate_id_usuario(cls, v):
        if v <= 0:
            raise ValueError('id_usuario debe ser positivo')
        return v

class DocenteRead(BaseModel):
    id_docente: int
    especialidad: Optional[str]
    grado_academico: Optional[str]
    anios_experiencia: Optional[int]
    fecha_inicio: Optional[date]
    estado: Optional[str]
    created_at: datetime
    updated_at: datetime
    ci: str
    nombre: str
    ape_paterno: str
    ape_materno: str
    correo_electronico: str

    class Config:
        from_attributes = True

class DocenteUpdate(BaseModel):
    especialidad: Optional[str] = Field(None, max_length=100)
    grado_academico: Optional[str] = Field(None, max_length=100)
    anios_experiencia: Optional[int] = Field(None, ge=0)
    fecha_inicio: Optional[date] = None
    estado: Optional[str] = Field(None, pattern="^(activo|inactivo)$")