from sqlalchemy import Column, Integer, String, Date, Text, ForeignKey
from app.core.database import Base
class Asistencia(Base):
    __tablename__ = "asistencia"
    __table_args__ = {"extend_existing": True}
    id_asistencia = Column(Integer, primary_key=True, index=True)
    id_inscripcion = Column(Integer, ForeignKey("inscripcion.id_inscripcion", ondelete="RESTRICT"), nullable=False, index=True)
    fecha_asistencia = Column(Date, nullable=False)
    estado = Column(String(20))
    observaciones = Column(Text)