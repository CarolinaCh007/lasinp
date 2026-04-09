from sqlalchemy import Column, Integer, String, Date, Time, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class LogAuditoria(Base):
    __tablename__ = "log_auditoria"
    id_log = Column(Integer, primary_key=True, index=True)
    id_usuario = Column(Integer, ForeignKey("usuario.id_usuario"), nullable=False)
    accion = Column(String(50), nullable=False)
    tabla_afectada = Column(String(50))
    direccion_ip = Column(String(45))
    fecha = Column(Date)
    hora = Column(Time)

    usuario = relationship("Usuario")