from pydantic import BaseModel, Field
from typing import Optional
from datetime import date, time, datetime
from decimal import Decimal

class PagoCreate(BaseModel):
    id_inscripcion: int
    precio: Optional[Decimal] = Field(None, ge=0)
    fecha_pago: Optional[date] = None
    hora_pago: Optional[time] = None
    estado: Optional[str] = Field("pendiente", pattern="^(pagado|pendiente|no realizado)$")
    metodo_pago: Optional[str] = Field(None, max_length=50)
    id_transaccion_lib: Optional[str] = None
    codigo_recaudacion: Optional[str] = None
    observaciones: Optional[str] = None
    url_pasarela: Optional[str] = None
    identificador_deuda: Optional[str] = None
    ci_nit_facturacion: Optional[str] = Field(None, max_length=20)

class PagoUpdate(BaseModel):
    id_inscripcion: Optional[int] = None
    precio: Optional[Decimal] = Field(None, ge=0)
    fecha_pago: Optional[date] = None
    hora_pago: Optional[time] = None
    estado: Optional[str] = Field(None, pattern="^(pagado|pendiente|no realizado)$")
    metodo_pago: Optional[str] = Field(None, max_length=50)
    id_transaccion_lib: Optional[str] = None
    codigo_recaudacion: Optional[str] = None
    observaciones: Optional[str] = None
    url_pasarela: Optional[str] = None
    identificador_deuda: Optional[str] = None
    ci_nit_facturacion: Optional[str] = Field(None, max_length=20)

class PagoRead(BaseModel):
    id_pago: int; id_inscripcion: int; precio: Optional[Decimal]
    fecha_pago: Optional[date]; hora_pago: Optional[time]; estado: str
    metodo_pago: Optional[str]; id_transaccion_lib: Optional[str]
    codigo_recaudacion: Optional[str]; observaciones: Optional[str]
    url_pasarela: Optional[str]; identificador_deuda: Optional[str]
    ci_nit_facturacion: Optional[str]; created_at: datetime; updated_at: datetime
    class Config: from_attributes = True