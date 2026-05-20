from sqlalchemy import Column, Integer, Numeric, DateTime, ForeignKey, func
from app.core.database import Base
class Calificacion(Base):
    __tablename__ = "calificacion"
    __table_args__ = {"extend_existing": True}
    id_nota = Column(Integer, primary_key=True, index=True)
    id_inscripcion = Column(Integer, ForeignKey("inscripcion.id_inscripcion", ondelete="RESTRICT"), nullable=False, index=True)
    id_tipo = Column(Integer, ForeignKey("tipo_evaluacion.id_tipo", ondelete="RESTRICT"), nullable=False)
    puntaje = Column(Numeric(5, 2))
    fecha_registro = Column(DateTime, server_default=func.now())