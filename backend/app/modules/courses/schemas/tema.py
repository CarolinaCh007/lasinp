from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class TemaCreate(BaseModel):
    id_curso: int
    numero_tema: Optional[int] = Field(None, gt=0)
    titulo: str = Field(..., max_length=100)
    descripcion: Optional[str] = None
    duracion_estimada: Optional[str] = Field(None, max_length=50)

class TemaUpdate(BaseModel):
    id_curso: Optional[int] = None
    numero_tema: Optional[int] = Field(None, gt=0)
    titulo: Optional[str] = Field(None, max_length=100)
    descripcion: Optional[str] = None
    duracion_estimada: Optional[str] = Field(None, max_length=50)

class TemaRead(BaseModel):
    id_tema: int; id_curso: int; numero_tema: Optional[int]; titulo: str
    descripcion: Optional[str]; duracion_estimada: Optional[str]
    class Config: from_attributes = True