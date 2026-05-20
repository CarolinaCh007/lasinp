from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
class EncuestaSatisfaccionCreate(BaseModel):
    id_inscripcion: int; calificacion_curso: int = Field(..., ge=1, le=5)
    calificacion_docente: int = Field(..., ge=1, le=5); comentarios: Optional[str] = None
class EncuestaSatisfaccionRead(BaseModel):
    id_encuesta: int; id_inscripcion: int; calificacion_curso: int; calificacion_docente: int
    comentarios: Optional[str]; fecha: datetime
    class Config: from_attributes = True