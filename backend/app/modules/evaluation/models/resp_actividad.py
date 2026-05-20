from sqlalchemy import Column, Integer, Text, Date, Time, ForeignKey
from app.core.database import Base
class RespActividad(Base):
    __tablename__ = "resp_actividad"
    __table_args__ = {"extend_existing": True}
    id_resp = Column(Integer, primary_key=True, index=True)
    id_inscripcion = Column(Integer, ForeignKey("inscripcion.id_inscripcion", ondelete="RESTRICT"), nullable=False)
    link_repositorio = Column(Text)
    fecha_entrega = Column(Date)
    hora_entrega = Column(Time)
    comentario = Column(Text)