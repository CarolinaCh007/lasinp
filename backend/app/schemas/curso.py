from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional
from decimal import Decimal

class CursoCreate(BaseModel):
    nombre: str
    sigla: Optional[str] = None
    especialidad: Optional[str] = None
    descripcion: Optional[str] = None
    objetivo: Optional[str] = None
    fecha_inicio: Optional[date] = None
    fecha_fin: Optional[date] = None
    nivel: Optional[str] = None
    carga_horaria: Optional[int] = None
    costo: Optional[Decimal] = None
    cupos_totales: Optional[int] = None
    imagen_url: Optional[str] = None
    duracion: Optional[str] = None
    link_whatsapp: Optional[str] = None
    requisitos_tecnicos: Optional[str] = None
    requisitos_previos: Optional[str] = None

class CursoResponse(BaseModel):
    id_curso: int
    nombre: str
    sigla: Optional[str] = None
    especialidad: Optional[str] = None
    descripcion: Optional[str] = None
    objetivo: Optional[str] = None
    fecha_inicio: Optional[date] = None
    fecha_fin: Optional[date] = None
    nivel: Optional[str] = None
    carga_horaria: Optional[int] = None
    costo: Optional[Decimal] = None
    cupos_totales: Optional[int] = None
    imagen_url: Optional[str] = None
    duracion: Optional[str] = None
    link_whatsapp: Optional[str] = None
    estado: Optional[str] = None
    created_at: Optional[datetime] = None
    requisitos_tecnicos: Optional[str] = None
    requisitos_previos: Optional[str] = None

    class Config:
        from_attributes = True

class CursoUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    objetivo: Optional[str] = None
    fecha_inicio: Optional[date] = None
    fecha_fin: Optional[date] = None
    costo: Optional[Decimal] = None
    cupos_totales: Optional[int] = None
    imagen_url: Optional[str] = None
    link_whatsapp: Optional[str] = None
    estado: Optional[str] = None
    requisitos_tecnicos: Optional[str] = None
    requisitos_previos: Optional[str] = None