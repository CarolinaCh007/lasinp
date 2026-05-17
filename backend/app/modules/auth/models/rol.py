from sqlalchemy import Column, Integer, String
from app.core.database import Base

class Rol(Base):
    __tablename__ = "rol"

    id_rol = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), unique=True, nullable=False, index=True)  # ej: "ADMIN", "DOCENTE"
    descripcion = Column(String(255), nullable=True)

    def __repr__(self):
        return f"<Rol(id={self.id_rol}, nombre='{self.nombre}')>"