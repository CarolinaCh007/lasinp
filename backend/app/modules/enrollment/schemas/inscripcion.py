from pydantic import BaseModel, Field
from typing import Optional
from datetime import date, time, datetime
from .pago import PagoCreate
from decimal import Decimal

class InscripcionCreate(BaseModel):
    id_horario: int
    id_estudiante: int
    fecha_inscripcion: Optional[date] = None
    hora_inscripcion: Optional[time] = None
    estado: Optional[str] = Field("pendiente", pattern="^(activo|inactivo|pendiente|retirado)$")
    nota_final: Optional[Decimal] = Field(None, ge=0, le=100)

class InscripcionUpdate(BaseModel):
    id_horario: Optional[int] = None
    id_estudiante: Optional[int] = None
    fecha_inscripcion: Optional[date] = None
    hora_inscripcion: Optional[time] = None
    estado: Optional[str] = Field(None, pattern="^(activo|inactivo|pendiente|retirado)$")
    nota_final: Optional[Decimal] = Field(None, ge=0, le=100)

class InscripcionRead(BaseModel):
    id_inscripcion: int; id_horario: int; id_estudiante: int
    fecha_inscripcion: Optional[date]; hora_inscripcion: Optional[time]
    estado: Optional[str]; nota_final: Optional[Decimal]
    created_at: datetime; updated_at: datetime
    class Config: from_attributes = True

class InscripcionConPagoRequest(BaseModel):
    """Solicitud para inscribirse + subir comprobante del primer pago en un solo paso"""
    inscripcion: InscripcionCreate
    pago: PagoCreate