from sqlalchemy import Column, Integer, String, Date, DateTime, Time, Text, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Inscripcion(Base):
    __tablename__ = "inscripcion"
    id_inscripcion = Column(Integer, primary_key=True, index=True)
    id_horario = Column(Integer, ForeignKey("horario.id_horario"), nullable=False)
    id_estudiante = Column(Integer, ForeignKey("estudiante.id_estudiante"), nullable=False)
    fecha_inscripcion = Column(Date)
    hora_inscripcion = Column(Time)
    estado = Column(String(20), default="pendiente")
    nota_final = Column(Numeric(5,2))
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    horario = relationship("Horario", back_populates="inscripciones")
    estudiante = relationship("Estudiante", back_populates="inscripciones")
    pagos = relationship("Pago", back_populates="inscripcion")
    asistencias = relationship("Asistencia", back_populates="inscripcion")
    calificaciones = relationship("Calificacion", back_populates="inscripcion")
    certificado = relationship("Certificado", back_populates="inscripcion", uselist=False)
    encuesta = relationship("EncuestaSatisfaccion", back_populates="inscripcion", uselist=False)
    respuestas = relationship("RespActividad", back_populates="inscripcion")

class Pago(Base):
    __tablename__ = "pago"
    id_pago = Column(Integer, primary_key=True, index=True)
    id_inscripcion = Column(Integer, ForeignKey("inscripcion.id_inscripcion"), nullable=False)
    precio = Column(Numeric(10,2))
    fecha_pago = Column(Date)
    hora_pago = Column(Time)
    estado = Column(String(20), default="pendiente")
    metodo_pago = Column(String(50))
    id_transaccion_lib = Column(Text)
    codigo_recaudacion = Column(Text)
    observaciones = Column(Text)
    url_pasarela = Column(Text)
    identificador_deuda = Column(Text)
    ci_nit_facturacion = Column(String(20))
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    inscripcion = relationship("Inscripcion", back_populates="pagos")
class Asistencia(Base):
    __tablename__ = "asistencia"
    id_asistencia = Column(Integer, primary_key=True, index=True)
    id_inscripcion = Column(Integer, ForeignKey("inscripcion.id_inscripcion"), nullable=False)
    fecha_asistencia = Column(Date, nullable=False)
    estado = Column(String(20))
    observaciones = Column(Text)

    inscripcion = relationship("Inscripcion", back_populates="asistencias")

class TipoEvaluacion(Base):
    __tablename__ = "tipo_evaluacion"
    id_tipo = Column(Integer, primary_key=True, index=True)
    id_curso = Column(Integer, ForeignKey("curso.id_curso"), nullable=False)
    nombre = Column(String(100), nullable=False)
    peso_porcentual = Column(Numeric(5,2))

    curso = relationship("Curso", back_populates="tipos_evaluacion")
    calificaciones = relationship("Calificacion", back_populates="tipo")

class Calificacion(Base):
    __tablename__ = "calificacion"
    id_nota = Column(Integer, primary_key=True, index=True)
    id_inscripcion = Column(Integer, ForeignKey("inscripcion.id_inscripcion"), nullable=False)
    id_tipo = Column(Integer, ForeignKey("tipo_evaluacion.id_tipo"), nullable=False)
    puntaje = Column(Numeric(5,2))
    fecha_registro = Column(DateTime, default=datetime.now)

    inscripcion = relationship("Inscripcion", back_populates="calificaciones")
    tipo = relationship("TipoEvaluacion", back_populates="calificaciones")