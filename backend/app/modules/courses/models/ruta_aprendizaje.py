from sqlalchemy import Column, Integer, String, Text
from app.core.database import Base

class RutaAprendizaje(Base):
    __tablename__ = "ruta_aprendizaje"
    __table_args__ = {"extend_existing": True}
    id_ruta = Column(Integer, primary_key=True, index=True)
    nombre_ruta = Column(String(100), nullable=False)
    descripcion = Column(Text)
    habilidades = Column(Text)
    imagen_url = Column(Text)