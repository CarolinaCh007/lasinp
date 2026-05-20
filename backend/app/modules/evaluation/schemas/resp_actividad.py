from pydantic import BaseModel, Field
from typing import Optional
from datetime import date, time
class RespActividadCreate(BaseModel):
    id_inscripcion: int; link_repositorio: Optional[str] = None
    fecha_entrega: Optional[date] = None; hora_entrega: Optional[time] = None; comentario: Optional[str] = None
class RespActividadUpdate(BaseModel):
    link_repositorio: Optional[str] = None; fecha_entrega: Optional[date] = None
    hora_entrega: Optional[time] = None; comentario: Optional[str] = None
class RespActividadRead(BaseModel):
    id_resp: int; id_inscripcion: int; link_repositorio: Optional[str]
    fecha_entrega: Optional[date]; hora_entrega: Optional[time]; comentario: Optional[str]
    class Config: from_attributes = True