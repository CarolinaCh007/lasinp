from sqlalchemy import Column, Integer, String, Boolean, Date, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Rol(Base):
    __tablename__ = "rol"
    id_rol = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), nullable=False, unique=True)
    descripcion = Column(Text)

class Usuario(Base):
    __tablename__ = "usuario"
    id_usuario = Column(Integer, primary_key=True, index=True)
    ci = Column(String(20), unique=True)
    correo_electronico = Column(String(100), nullable=False, unique=True)
    password = Column(Text, nullable=False)
    nombre = Column(String(50), nullable=False)
    ape_paterno = Column(String(50))
    ape_materno = Column(String(50))
    celular = Column(String(20))
    fecha_nacimiento = Column(Date)
    direccion = Column(Text)
    sexo = Column(String(10))
    foto_perfil = Column(Text)
    estado = Column(String(20), default="pendiente")
    fecha_registro = Column(DateTime, default=datetime.now)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    instancias = relationship("Instancia", back_populates="usuario")
    estudiante = relationship("Estudiante", back_populates="usuario", uselist=False)
    docente = relationship("Docente", back_populates="usuario", uselist=False)

class Instancia(Base):
    __tablename__ = "instancia"
    id_usuario = Column(Integer, ForeignKey("usuario.id_usuario"), primary_key=True)
    id_rol = Column(Integer, ForeignKey("rol.id_rol"), primary_key=True)
    fecha_asignacion = Column(Date)

    usuario = relationship("Usuario", back_populates="instancias")
    rol = relationship("Rol")