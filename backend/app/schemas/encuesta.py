from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class EncuestaCreate(BaseModel):
    id_inscripcion: int
    calificacion_curso: int
    calificacion_docente: int
    comentarios: Optional[str] = None

class EncuestaResponse(BaseModel):
    id_encuesta: int
    id_inscripcion: int
    calificacion_curso: Optional[int] = None
    calificacion_docente: Optional[int] = None
    comentarios: Optional[str] = None
    fecha: Optional[datetime] = None

    class Config:
        from_attributes = True