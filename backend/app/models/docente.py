from sqlalchemy import Column, Integer, String, Date, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Docente(Base):
    __tablename__ = "docente"
    id_docente = Column(Integer, primary_key=True, index=True)
    id_usuario = Column(Integer, ForeignKey("usuario.id_usuario"), unique=True, nullable=False)
    especialidad = Column(String(100))
    grado_academico = Column(String(100))
    anios_experiencia = Column(Integer)
    fecha_inicio = Column(Date)
    estado = Column(String(20))
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    usuario = relationship("Usuario", back_populates="docente")
    portafolio = relationship("Portafolio", back_populates="docente", uselist=False)
    horarios = relationship("Horario", back_populates="docente")

class Portafolio(Base):
    __tablename__ = "portafolio"
    id_portafolio = Column(Integer, primary_key=True, index=True)
    id_docente = Column(Integer, ForeignKey("docente.id_docente"), unique=True, nullable=False)
    direccion_cv = Column(Text)
    linkedin = Column(Text)
    github = Column(Text)

    docente = relationship("Docente", back_populates="portafolio")