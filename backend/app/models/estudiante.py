from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Estudiante(Base):
    __tablename__ = "estudiante"
    id_estudiante = Column(Integer, primary_key=True, index=True)
    id_usuario = Column(Integer, ForeignKey("usuario.id_usuario"), unique=True, nullable=False)
    nivel = Column(String(50))
    institucion = Column(String(100))
    fecha_ingreso = Column(Date)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    usuario = relationship("Usuario", back_populates="estudiante")
    inscripciones = relationship("Inscripcion", back_populates="estudiante")