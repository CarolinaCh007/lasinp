from pydantic import BaseModel, Field
from typing import Optional
from datetime import date
class AsistenciaCreate(BaseModel):
    id_inscripcion: int; fecha_asistencia: date; estado: str = Field(..., pattern="^(presente|ausente|justificado)$")
    observaciones: Optional[str] = None
class AsistenciaUpdate(BaseModel):
    estado: Optional[str] = Field(None, pattern="^(presente|ausente|justificado)$"); observaciones: Optional[str] = None
class AsistenciaRead(BaseModel):
    id_asistencia: int; id_inscripcion: int; fecha_asistencia: date; estado: str; observaciones: Optional[str]
    class Config: from_attributes = True