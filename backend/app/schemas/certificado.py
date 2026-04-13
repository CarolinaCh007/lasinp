from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional

class CertificadoCreate(BaseModel):
    id_inscripcion: int
    codigo_verificacion: str

class CertificadoResponse(BaseModel):
    id_certificado: int
    id_inscripcion: int
    codigo_verificacion: str
    fecha_emision: Optional[date] = None
    qr_url: Optional[str] = None
    estado: Optional[str] = None
    hash_certificado: Optional[str] = None
    url_certificado: Optional[str] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class CertificadoUpdate(BaseModel):
    estado: Optional[str] = None
    qr_url: Optional[str] = None
    url_certificado: Optional[str] = None

class VerificarCertificadoRequest(BaseModel):
    codigo_verificacion: str

class VerificarCertificadoResponse(BaseModel):
    valido: bool
    mensaje: str
    certificado: Optional[CertificadoResponse] = None