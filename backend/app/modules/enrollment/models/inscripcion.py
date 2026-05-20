from sqlalchemy import Column, Integer, Date, Time, String, Numeric, DateTime, ForeignKey, func
from app.core.database import Base

class Inscripcion(Base):
    __tablename__ = "inscripcion"
    __table_args__ = {"extend_existing": True}
    
    id_inscripcion = Column(Integer, primary_key=True, index=True)
    id_horario = Column(Integer, ForeignKey("horario.id_horario", ondelete="RESTRICT"), nullable=False, index=True)
    id_estudiante = Column(Integer, ForeignKey("estudiante.id_estudiante", ondelete="RESTRICT"), nullable=False, index=True)
    fecha_inscripcion = Column(Date, server_default=func.current_date())
    hora_inscripcion = Column(Time, server_default=func.current_time())
    estado = Column(String(20))
    nota_final = Column(Numeric(5, 2))
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())