from sqlalchemy import Column, Integer, String, Date, DateTime, func
from sqlalchemy.orm import relationship
from app.core.database import Base

class Usuario(Base):
    __tablename__ = "usuario"
    __table_args__ = {"extend_existing": True}
    
    id_usuario = Column(Integer, primary_key=True, index=True)
    ci = Column(String(20), unique=True, index=True, nullable=False)
    correo_electronico = Column(String(100), unique=True, nullable=False, index=True)
    password = Column(String(255), nullable=False)
    nombre = Column(String(50), nullable=False)
    ape_paterno = Column(String(50))
    ape_materno = Column(String(50))
    celular = Column(String(20))
    fecha_nacimiento = Column(Date)
    direccion = Column(String)
    sexo = Column(String(10))
    foto_perfil = Column(String)
    estado = Column(String(20), default="pendiente", server_default="pendiente")
    fecha_registro = Column(DateTime, server_default=func.now())
    ultimo_acceso = Column(DateTime, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    instancias = relationship("Instancia", back_populates="usuario", lazy="select")
    
    # ❌ ELIMINAR relaciones hacia academic/:
    # estudiante = relationship(...)  ← BORRAR
    # docente = relationship(...)     ← BORRAR

    def __repr__(self):
        return f"<Usuario(id={self.id_usuario}, email='{self.correo_electronico}')>"