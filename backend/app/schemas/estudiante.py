from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional

class EstudianteCreate(BaseModel):
    id_usuario: int
    nivel: Optional[str] = None
    institucion: Optional[str] = None

class EstudianteResponse(BaseModel):
    id_estudiante: int
    id_usuario: int
    nivel: Optional[str] = None
    institucion: Optional[str] = None
    fecha_ingreso: Optional[date] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class EstudianteUpdate(BaseModel):
    nivel: Optional[str] = None
    institucion: Optional[str] = None