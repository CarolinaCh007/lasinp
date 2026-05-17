from sqlalchemy import Column, Integer, String, Time, DateTime, ForeignKey, func
from app.core.database import Base

class Horario(Base):
    __tablename__ = "horario"
    __table_args__ = {"extend_existing": True}
    
    id_horario = Column(Integer, primary_key=True, index=True)
    id_curso = Column(Integer, ForeignKey("curso.id_curso", ondelete="RESTRICT"), nullable=False, index=True)
    id_aula = Column(Integer, ForeignKey("aula.id_aula", ondelete="SET NULL"))
    id_docente = Column(Integer, ForeignKey("docente.id_docente", ondelete="SET NULL"))
    grupo = Column(String(10))
    dia_semana = Column(String(20))
    hora_inicio = Column(Time)
    hora_fin = Column(Time)
    estado = Column(String(20), default="activo")
    cantidad_dias = Column(Integer)
    modalidad = Column(String(20))
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())