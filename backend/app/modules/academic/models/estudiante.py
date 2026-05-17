from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey, func
from app.core.database import Base

class Estudiante(Base):
    __tablename__ = "estudiante"
    __table_args__ = {"extend_existing": True}
    
    id_estudiante = Column(Integer, ForeignKey("usuario.id_usuario", ondelete="CASCADE"), primary_key=True, index=True)
    institucion = Column(String(100), nullable=True)
    fecha_ingreso = Column(Date, nullable=True, server_default=func.current_date())
    created_at = Column(DateTime, nullable=False, server_default=func.current_timestamp())
    updated_at = Column(DateTime, nullable=False, server_default=func.current_timestamp(), onupdate=func.current_timestamp())

    # 🔹 SIN relationship hacia Usuario → cero conflictos