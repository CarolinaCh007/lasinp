from sqlalchemy import Column, Integer, String, Date, DateTime, Text, Numeric, Time, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Curso(Base):
    __tablename__ = "curso"
    id_curso = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    sigla = Column(String(20), unique=True)
    especialidad = Column(String(100))
    descripcion = Column(Text)
    objetivo = Column(Text)
    fecha_inicio = Column(Date)
    fecha_fin = Column(Date)
    nivel = Column(String(50))
    carga_horaria = Column(Integer)
    costo = Column(Numeric(10,2))
    cupos_totales = Column(Integer)
    imagen_url = Column(Text)
    duracion = Column(String(50))
    estado = Column(String(20), default="pendiente")
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    link_whatsapp = Column(Text)

    horarios = relationship("Horario", back_populates="curso")
    temas = relationship("Tema", back_populates="curso")
    tipos_evaluacion = relationship("TipoEvaluacion", back_populates="curso")
    rutas = relationship("RutaTiene", back_populates="curso")

class RutaAprendizaje(Base):
    __tablename__ = "ruta_aprendizaje"
    id_ruta = Column(Integer, primary_key=True, index=True)
    nombre_ruta = Column(String(100), nullable=False)
    descripcion = Column(Text)
    habilidades = Column(Text)
    imagen_url = Column(Text)

    cursos = relationship("RutaTiene", back_populates="ruta")

class RutaTiene(Base):
    __tablename__ = "ruta_tiene"
    id_ruta = Column(Integer, ForeignKey("ruta_aprendizaje.id_ruta"), primary_key=True)
    id_curso = Column(Integer, ForeignKey("curso.id_curso"), primary_key=True)

    ruta = relationship("RutaAprendizaje", back_populates="cursos")
    curso = relationship("Curso", back_populates="rutas")

class Aula(Base):
    __tablename__ = "aula"
    id_aula = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), nullable=False)
    ubicacion = Column(Text)
    capacidad = Column(Integer)
    enlace_teams = Column(Text)

    horarios = relationship("Horario", back_populates="aula")

class Horario(Base):
    __tablename__ = "horario"
    id_horario = Column(Integer, primary_key=True, index=True)
    id_curso = Column(Integer, ForeignKey("curso.id_curso"), nullable=False)
    id_aula = Column(Integer, ForeignKey("aula.id_aula"))
    id_docente = Column(Integer, ForeignKey("docente.id_docente"))
    grupo = Column(String(10))
    dia_semana = Column(String(20))
    hora_inicio = Column(Time)
    hora_fin = Column(Time)
    estado = Column(String(20))
    cantidad_dias = Column(Integer)
    modalidad = Column(String(20))
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    curso = relationship("Curso", back_populates="horarios")
    aula = relationship("Aula", back_populates="horarios")
    docente = relationship("Docente", back_populates="horarios")
    inscripciones = relationship("Inscripcion", back_populates="horario")
    actividades = relationship("ActividadFinal", back_populates="horario")

class Tema(Base):
    __tablename__ = "tema"
    id_tema = Column(Integer, primary_key=True, index=True)
    id_curso = Column(Integer, ForeignKey("curso.id_curso"), nullable=False)
    numero_tema = Column(Integer)
    titulo = Column(String(100), nullable=False)
    descripcion = Column(Text)
    duracion_estimada = Column(String(50))

    curso = relationship("Curso", back_populates="temas")