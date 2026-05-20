from sqlalchemy import Column, Integer, String, Text, Date, Time, ForeignKey
from app.core.database import Base
class ActividadFinal(Base):
    __tablename__ = "actividad_final"
    __table_args__ = {"extend_existing": True}
    id_actividad = Column(Integer, primary_key=True, index=True)
    id_horario = Column(Integer, ForeignKey("horario.id_horario", ondelete="RESTRICT"), nullable=False)
    nombre_act = Column(String(100))
    instruccion = Column(Text)
    fecha_limite = Column(Date)
    hora_limite = Column(Time)