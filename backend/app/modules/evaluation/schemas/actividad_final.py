from pydantic import BaseModel, Field
from typing import Optional
from datetime import date, time
class ActividadFinalCreate(BaseModel):
    id_horario: int; nombre_act: Optional[str] = Field(None, max_length=100)
    instruccion: Optional[str] = None; fecha_limite: Optional[date] = None; hora_limite: Optional[time] = None
class ActividadFinalUpdate(BaseModel):
    nombre_act: Optional[str] = Field(None, max_length=100); instruccion: Optional[str] = None
    fecha_limite: Optional[date] = None; hora_limite: Optional[time] = None
class ActividadFinalRead(BaseModel):
    id_actividad: int; id_horario: int; nombre_act: Optional[str]; instruccion: Optional[str]
    fecha_limite: Optional[date]; hora_limite: Optional[time]
    class Config: from_attributes = True