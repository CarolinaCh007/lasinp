from pydantic import BaseModel, Field

class RutaTieneCreate(BaseModel):
    id_ruta: int
    id_curso: int

class RutaTieneRead(BaseModel):
    id_ruta: int; id_curso: int
    class Config: from_attributes = True