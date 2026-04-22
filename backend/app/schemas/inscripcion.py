from pydantic import BaseModel
from datetime import date, time, datetime
from typing import Optional
from decimal import Decimal

class InscripcionCreate(BaseModel):
    id_horario: int
    id_estudiante: int

class InscripcionResponse(BaseModel):
    id_inscripcion: int
    id_horario: int
    id_estudiante: int
    fecha_inscripcion: Optional[date] = None
    hora_inscripcion: Optional[time] = None
    estado: Optional[str] = None
    nota_final: Optional[Decimal] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class InscripcionUpdate(BaseModel):
    estado: Optional[str] = None
    nota_final: Optional[Decimal] = None

class PagoCreate(BaseModel):
    id_inscripcion: int
    precio: Decimal
    metodo_pago: Optional[str] = None
    identificador_deuda: Optional[str] = None
    ci_nit_facturacion: Optional[str] = None

class PagoResponse(BaseModel):
    id_pago: int
    id_inscripcion: int
    precio: Optional[Decimal] = None
    fecha_pago: Optional[date] = None
    hora_pago: Optional[time] = None
    estado: Optional[str] = None
    metodo_pago: Optional[str] = None
    codigo_recaudacion: Optional[str] = None
    url_pasarela: Optional[str] = None
    ci_nit_facturacion: Optional[str] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class PagoUpdate(BaseModel):
    estado: Optional[str] = None
    codigo_recaudacion: Optional[str] = None
    id_transaccion_lib: Optional[str] = None
    observaciones: Optional[str] = None