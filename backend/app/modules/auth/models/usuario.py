from sqlalchemy import Column, Integer, String, Date, DateTime, Text, func, CheckConstraint
from sqlalchemy.orm import relationship
from app.core.database import Base

class Usuario(Base):
    __tablename__ = "usuario"
    
    # ✅ Permite recargar modelos sin conflicto (desarrollo con --reload)
    __table_args__ = (
        CheckConstraint(
            "estado IN ('activo', 'inactivo', 'pendiente', 'bloqueado')",
            name="usuario_estado_check"
        ),
        CheckConstraint(
            "sexo IN ('M', 'F', 'Otro')",
            name="usuario_sexo_check"
        ),
        {"extend_existing": True}
    )
    
    # 🔹 Columnas primarias y de identificación
    id_usuario = Column(Integer, primary_key=True, index=True)
    ci = Column(String(20), unique=True, index=True, nullable=True)
    correo_electronico = Column(String(100), unique=True, nullable=False, index=True)
    
    # 🔹 Autenticación
    password = Column(Text, nullable=False)  # ← Text, no String(255)
    
    # 🔹 Datos personales
    nombre = Column(String(50), nullable=False)
    ape_paterno = Column(String(50), nullable=True)
    ape_materno = Column(String(50), nullable=True)
    celular = Column(String(20), nullable=True)
    fecha_nacimiento = Column(Date, nullable=True)
    direccion = Column(Text, nullable=True)  # ← Text, no String
    sexo = Column(String(10), nullable=True)  # CHECK: 'M', 'F', 'Otro'
    foto_perfil = Column(Text, nullable=True)  # ← Text, no String
    
    # 🔹 Estado y fechas
    estado = Column(String(20), nullable=True, server_default="pendiente")  # CHECK: valores permitidos
    fecha_registro = Column(DateTime, nullable=True, server_default=func.now())
    # ❌ ultimo_acceso ELIMINADO (no existe en tu BD)
    created_at = Column(DateTime, nullable=True, server_default=func.now())
    updated_at = Column(DateTime, nullable=True, server_default=func.now(), onupdate=func.now())

    # 🔹 Relaciones (solo intra-módulo auth/ para evitar conflictos)
    instancias = relationship("Instancia", back_populates="usuario", lazy="select")
    
    # ❌ Sin relaciones hacia academic/ (se consultan manualmente en servicios)

    def __repr__(self):
        return f"<Usuario(id={self.id_usuario}, email='{self.correo_electronico}', estado='{self.estado}')>"