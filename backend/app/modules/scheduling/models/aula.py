from sqlalchemy import Column, Integer, String, Text
from app.core.database import Base

class Aula(Base):
    __tablename__ = "aula"
    __table_args__ = {"extend_existing": True}
    
    id_aula = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), nullable=False)
    ubicacion = Column(Text)
    capacidad = Column(Integer)
    enlace_teams = Column(Text)