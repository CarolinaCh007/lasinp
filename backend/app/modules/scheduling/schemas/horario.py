from pydantic import BaseModel, Field
from typing import Optional
from datetime import time, datetime

class HorarioCreate(BaseModel):
    id_curso: int
    id_aula: Optional[int] = None
    id_docente: Optional[int] = None
    grupo: Optional[str] = Field(None, max_length=10)
    dia_semana: Optional[str] = Field(None, max_length=20)
    hora_inicio: Optional[time] = None
    hora_fin: Optional[time] = None
    estado: Optional[str] = Field("activo", pattern="^(activo|inactivo)$")
    cantidad_dias: Optional[int] = Field(None, ge=0)
    modalidad: Optional[str] = Field(None, pattern="^(presencial|virtual|hibrido)$")

class HorarioUpdate(BaseModel):
    id_curso: Optional[int] = None
    id_aula: Optional[int] = None
    id_docente: Optional[int] = None
    grupo: Optional[str] = Field(None, max_length=10)
    dia_semana: Optional[str] = Field(None, max_length=20)
    hora_inicio: Optional[time] = None
    hora_fin: Optional[time] = None
    estado: Optional[str] = Field(None, pattern="^(activo|inactivo)$")
    cantidad_dias: Optional[int] = Field(None, ge=0)
    modalidad: Optional[str] = Field(None, pattern="^(presencial|virtual|hibrido)$")

class HorarioRead(BaseModel):
    id_horario: int
    id_curso: int
    id_aula: Optional[int]
    id_docente: Optional[int]
    grupo: Optional[str]
    dia_semana: Optional[str]
    hora_inicio: Optional[time]
    hora_fin: Optional[time]
    estado: str
    cantidad_dias: Optional[int]
    modalidad: Optional[str]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True