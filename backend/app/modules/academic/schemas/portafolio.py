from pydantic import BaseModel, Field
from typing import Optional

class PortafolioCreate(BaseModel):
    id_docente: int = Field(..., gt=0, description="ID del docente asociado")
    direccion_cv: Optional[str] = None
    linkedin: Optional[str] = None
    github: Optional[str] = None

class PortafolioRead(BaseModel):
    id_portafolio: int
    id_docente: int
    direccion_cv: Optional[str]
    linkedin: Optional[str]
    github: Optional[str]

    class Config:
        from_attributes = True

class PortafolioUpdate(BaseModel):
    direccion_cv: Optional[str] = None
    linkedin: Optional[str] = None
    github: Optional[str] = None