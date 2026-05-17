from sqlalchemy import Column, Integer, String, Text, Date, Numeric, DateTime, func
from app.core.database import Base

class Curso(Base):
    __tablename__ = "curso"
    __table_args__ = {"extend_existing": True}
    id_curso = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    sigla = Column(String(20), unique=True)
    especialidad = Column(String(100))
    descripcion = Column(Text)
    objetivo = Column(Text)
    fecha_inicio = Column(Date)
    fecha_fin = Column(Date)
    nivel = Column(String(50))
    carga_horaria = Column(Integer)
    costo = Column(Numeric(10, 2))
    cupos_totales = Column(Integer)
    imagen_url = Column(Text)
    duracion = Column(String(50))
    estado = Column(String(20), default="pendiente", server_default="pendiente")
    link_whatsapp = Column(Text)
    requisitos_tecnicos = Column(Text)
    requisitos_previos = Column(Text)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())