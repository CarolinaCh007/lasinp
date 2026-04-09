from sqlalchemy import Column, Integer, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class EncuestaSatisfaccion(Base):
    __tablename__ = "encuesta_satisfaccion"
    id_encuesta = Column(Integer, primary_key=True, index=True)
    id_inscripcion = Column(Integer, ForeignKey("inscripcion.id_inscripcion"), unique=True, nullable=False)
    calificacion_curso = Column(Integer)
    calificacion_docente = Column(Integer)
    comentarios = Column(Text)
    fecha = Column(DateTime, default=datetime.now)

    inscripcion = relationship("Inscripcion", back_populates="encuesta")