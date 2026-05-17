from sqlalchemy import Column, Integer, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from app.core.database import Base

class Instancia(Base):
    __tablename__ = "instancia"

    # Clave primaria compuesta: Un usuario puede tener múltiples roles
    id_usuario = Column(Integer, ForeignKey("usuario.id_usuario", ondelete="CASCADE"), primary_key=True)
    id_rol = Column(Integer, ForeignKey("rol.id_rol", ondelete="CASCADE"), primary_key=True)
    fecha_asignacion = Column(DateTime, server_default=func.now())

    # Relaciones bidireccionales
    usuario = relationship("Usuario", back_populates="instancias")
    rol = relationship("Rol")

    def __repr__(self):
        return f"<Instancia(usuario={self.id_usuario}, rol={self.id_rol})>"