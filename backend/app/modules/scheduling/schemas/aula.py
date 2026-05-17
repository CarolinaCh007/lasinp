from pydantic import BaseModel, Field
from typing import Optional

class AulaCreate(BaseModel):
    nombre: str = Field(..., max_length=50)
    ubicacion: Optional[str] = None
    capacidad: Optional[int] = Field(None, gt=0)  # CHECK: capacidad > 0
    enlace_teams: Optional[str] = None

class AulaUpdate(BaseModel):
    nombre: Optional[str] = Field(None, max_length=50)
    ubicacion: Optional[str] = None
    capacidad: Optional[int] = Field(None, gt=0)
    enlace_teams: Optional[str] = None

class AulaRead(BaseModel):
    id_aula: int
    nombre: str
    ubicacion: Optional[str]
    capacidad: Optional[int]
    enlace_teams: Optional[str]
    
    class Config:
        from_attributes = True