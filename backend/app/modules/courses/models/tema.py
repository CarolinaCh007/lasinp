from sqlalchemy import Column, Integer, String, Text, ForeignKey
from app.core.database import Base

class Tema(Base):
    __tablename__ = "tema"
    __table_args__ = {"extend_existing": True}
    id_tema = Column(Integer, primary_key=True, index=True)
    id_curso = Column(Integer, ForeignKey("curso.id_curso", ondelete="RESTRICT"), nullable=False, index=True)
    numero_tema = Column(Integer)
    titulo = Column(String(100), nullable=False)
    descripcion = Column(Text)
    duracion_estimada = Column(String(50))