from pydantic import BaseModel, Field

class RolCreate(BaseModel):
    nombre: str = Field(..., max_length=50, description="Ej: ADMIN, DOCENTE, ESTUDIANTE")
    descripcion: str = Field(None, max_length=255)

class RolRead(BaseModel):
    id_rol: int
    nombre: str
    descripcion: str

    class Config:
        from_attributes = True