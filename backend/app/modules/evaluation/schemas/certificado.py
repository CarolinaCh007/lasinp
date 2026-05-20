from pydantic import BaseModel, Field
from typing import Optional
from datetime import date, datetime
class CertificadoRead(BaseModel):
    id_certificado: int; id_inscripcion: int; codigo_verificacion: str
    fecha_emision: date; qr_url: Optional[str]; estado: str = Field(..., pattern="^(emitido|anulado|pendiente)$")
    hash_certificado: Optional[str]; url_certificado: Optional[str]; created_at: datetime; updated_at: datetime
    class Config: from_attributes = True