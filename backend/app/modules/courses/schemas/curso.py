from pydantic import BaseModel, Field
from typing import Optional
from datetime import date, datetime
from decimal import Decimal

class CursoCreate(BaseModel):
    nombre: str = Field(..., max_length=100)
    sigla: Optional[str] = Field(None, max_length=20)
    especialidad: Optional[str] = Field(None, max_length=100)
    descripcion: Optional[str] = None
    objetivo: Optional[str] = None
    fecha_inicio: Optional[date] = None
    fecha_fin: Optional[date] = None
    nivel: Optional[str] = Field(None, max_length=50)
    carga_horaria: Optional[int] = Field(None, gt=0)
    costo: Optional[Decimal] = Field(None, ge=0)
    cupos_totales: Optional[int] = Field(None, gt=0)
    imagen_url: Optional[str] = None
    duracion: Optional[str] = Field(None, max_length=50)
    estado: Optional[str] = Field("pendiente", pattern="^(activo|inactivo|pendiente|archivado)$")
    link_whatsapp: Optional[str] = None
    requisitos_tecnicos: Optional[str] = None
    requisitos_previos: Optional[str] = None

class CursoUpdate(BaseModel):
    nombre: Optional[str] = Field(None, max_length=100)
    sigla: Optional[str] = Field(None, max_length=20)
    especialidad: Optional[str] = Field(None, max_length=100)
    descripcion: Optional[str] = None
    objetivo: Optional[str] = None
    fecha_inicio: Optional[date] = None
    fecha_fin: Optional[date] = None
    nivel: Optional[str] = Field(None, max_length=50)
    carga_horaria: Optional[int] = Field(None, gt=0)
    costo: Optional[Decimal] = Field(None, ge=0)
    cupos_totales: Optional[int] = Field(None, gt=0)
    imagen_url: Optional[str] = None
    duracion: Optional[str] = Field(None, max_length=50)
    estado: Optional[str] = Field(None, pattern="^(activo|inactivo|pendiente|archivado)$")
    link_whatsapp: Optional[str] = None
    requisitos_tecnicos: Optional[str] = None
    requisitos_previos: Optional[str] = None

class CursoRead(BaseModel):
    id_curso: int; nombre: str; sigla: Optional[str]; especialidad: Optional[str]
    descripcion: Optional[str]; objetivo: Optional[str]; fecha_inicio: Optional[date]; fecha_fin: Optional[date]
    nivel: Optional[str]; carga_horaria: Optional[int]; costo: Optional[Decimal]; cupos_totales: Optional[int]
    imagen_url: Optional[str]; duracion: Optional[str]; estado: str; link_whatsapp: Optional[str]
    requisitos_tecnicos: Optional[str]; requisitos_previos: Optional[str]
    created_at: datetime; updated_at: datetime
    class Config: from_attributes = True