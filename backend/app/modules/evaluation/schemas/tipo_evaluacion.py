from pydantic import BaseModel, Field
from typing import Optional
from decimal import Decimal
class TipoEvaluacionCreate(BaseModel):
    id_curso: int; nombre: str = Field(..., max_length=100)
    peso_porcentual: Optional[Decimal] = Field(None, ge=0, le=100)
class TipoEvaluacionRead(BaseModel):
    id_tipo: int; id_curso: int; nombre: str; peso_porcentual: Optional[Decimal]
    class Config: from_attributes = True