from sqlalchemy import Column, Integer, ForeignKey, String, DateTime, func
from app.core.database import Base

class LogAuditoria(Base):
    __tablename__ = "log_auditoria"

    id_log = Column(Integer, primary_key=True, index=True)
    id_usuario = Column(Integer, ForeignKey("usuario.id_usuario", ondelete="SET NULL"), nullable=True)
    accion = Column(String(50), nullable=False)  # ej: "LOGIN", "CREATE_USER", "UPDATE_ROL"
    tabla_afectada = Column(String(50), nullable=True)
    direccion_ip = Column(String(45), nullable=True)  # Soporta IPv6
    fecha = Column(DateTime, server_default=func.now())
    hora = Column(DateTime, server_default=func.now())  # Según tu esquema (redundante pero lo respetamos)

    def __repr__(self):
        return f"<Log(id={self.id_log}, accion='{self.accion}', usuario={self.id_usuario})>"