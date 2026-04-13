from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional

class DocenteCreate(BaseModel):
    id_usuario: int
    especialidad: Optional[str] = None
    grado_academico: Optional[str] = None
    anios_experiencia: Optional[int] = None
    fecha_inicio: Optional[date] = None

class DocenteResponse(BaseModel):
    id_docente: int
    id_usuario: int
    especialidad: Optional[str] = None
    grado_academico: Optional[str] = None
    anios_experiencia: Optional[int] = None
    fecha_inicio: Optional[date] = None
    estado: Optional[str] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class DocenteUpdate(BaseModel):
    especialidad: Optional[str] = None
    grado_academico: Optional[str] = None
    anios_experiencia: Optional[int] = None
    estado: Optional[str] = None

class PortafolioCreate(BaseModel):
    id_docente: int
    direccion_cv: Optional[str] = None
    linkedin: Optional[str] = None
    github: Optional[str] = None

class PortafolioResponse(BaseModel):
    id_portafolio: int
    id_docente: int
    direccion_cv: Optional[str] = None
    linkedin: Optional[str] = None
    github: Optional[str] = None

    class Config:
        from_attributes = True

class PortafolioUpdate(BaseModel):
    direccion_cv: Optional[str] = None
    linkedin: Optional[str] = None
    github: Optional[str] = None