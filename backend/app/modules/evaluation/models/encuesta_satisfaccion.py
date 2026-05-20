from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey, func
from app.core.database import Base
class EncuestaSatisfaccion(Base):
    __tablename__ = "encuesta_satisfaccion"
    __table_args__ = {"extend_existing": True}
    id_encuesta = Column(Integer, primary_key=True, index=True)
    id_inscripcion = Column(Integer, ForeignKey("inscripcion.id_inscripcion", ondelete="RESTRICT"), unique=True, nullable=False)
    calificacion_curso = Column(Integer)
    calificacion_docente = Column(Integer)
    comentarios = Column(Text)
    fecha = Column(DateTime, server_default=func.now())