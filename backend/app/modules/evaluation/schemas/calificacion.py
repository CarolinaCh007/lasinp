from pydantic import BaseModel, Field
from decimal import Decimal
from datetime import datetime
class CalificacionCreate(BaseModel):
    id_inscripcion: int; id_tipo: int; puntaje: Decimal = Field(..., ge=0, le=100)
class CalificacionRead(BaseModel):
    id_nota: int; id_inscripcion: int; id_tipo: int; puntaje: Decimal; fecha_registro: datetime
    class Config: from_attributes = True