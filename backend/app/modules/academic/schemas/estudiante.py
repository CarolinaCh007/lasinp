from pydantic import BaseModel, Field, field_validator  # ← ¡Agregar field_validator!
from typing import Optional
from datetime import date, datetime

# =============================================================================
# 🔹 SCHEMAS PARA ESTUDIANTE
# =============================================================================

class EstudianteCreate(BaseModel):
    """Datos para crear un perfil de estudiante"""
    id_usuario: int = Field(..., gt=0, description="ID del usuario base (debe ser el propio o ADMIN lo crea)")
    institucion: Optional[str] = Field(None, max_length=100)
    fecha_ingreso: Optional[date] = None

    @field_validator('id_usuario')
    @classmethod
    def validate_id_usuario(cls, v):
        if v <= 0:
            raise ValueError('id_usuario debe ser positivo')
        return v

class EstudianteRead(BaseModel):
    """Respuesta de API: perfil completo de estudiante"""
    id_estudiante: int
    institucion: Optional[str]
    fecha_ingreso: Optional[date]
    created_at: datetime
    updated_at: datetime
    # Datos unidos de usuario (obtenidos vía servicio)
    ci: str
    nombre: str
    ape_paterno: str
    ape_materno: str
    correo_electronico: str

    class Config:
        from_attributes = True

class EstudianteUpdate(BaseModel):
    """Datos para actualizar perfil de estudiante"""
    institucion: Optional[str] = Field(None, max_length=100)
    fecha_ingreso: Optional[date] = None