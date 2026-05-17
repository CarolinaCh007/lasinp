from pydantic import BaseModel, Field
from typing import Optional

class RutaAprendizajeCreate(BaseModel):
    nombre_ruta: str = Field(..., max_length=100)
    descripcion: Optional[str] = None
    habilidades: Optional[str] = None
    imagen_url: Optional[str] = None

class RutaAprendizajeUpdate(BaseModel):
    nombre_ruta: Optional[str] = Field(None, max_length=100)
    descripcion: Optional[str] = None
    habilidades: Optional[str] = None
    imagen_url: Optional[str] = None

class RutaAprendizajeRead(BaseModel):
    id_ruta: int; nombre_ruta: str; descripcion: Optional[str]; habilidades: Optional[str]; imagen_url: Optional[str]
    class Config: from_attributes = True