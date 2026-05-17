from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey, func, CheckConstraint
from app.core.database import Base

class Docente(Base):
    __tablename__ = "docente"
    __table_args__ = (
        CheckConstraint("anios_experiencia >= 0", name="docente_anios_experiencia_check"),
        CheckConstraint("estado IN ('activo', 'inactivo')", name="docente_estado_check"),
        {"extend_existing": True}
    )
    
    id_docente = Column(Integer, ForeignKey("usuario.id_usuario", ondelete="CASCADE"), primary_key=True, index=True)
    especialidad = Column(String(100), nullable=True)
    grado_academico = Column(String(100), nullable=True)
    anios_experiencia = Column(Integer, nullable=True)
    fecha_inicio = Column(Date, nullable=True)
    estado = Column(String(20), nullable=True)
    created_at = Column(DateTime, nullable=False, server_default=func.current_timestamp())
    updated_at = Column(DateTime, nullable=False, server_default=func.current_timestamp(), onupdate=func.current_timestamp())

    # 🔹 SIN relationships → cero conflictos