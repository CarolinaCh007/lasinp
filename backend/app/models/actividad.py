from sqlalchemy import Column, Integer, String, Date, Time, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class ActividadFinal(Base):
    __tablename__ = "actividad_final"
    id_actividad = Column(Integer, primary_key=True, index=True)
    id_horario = Column(Integer, ForeignKey("horario.id_horario"), nullable=False)
    instruccion = Column(Text)
    nombre_act = Column(String(100))
    fecha_limite = Column(Date)
    hora_limite = Column(Time)

    horario = relationship("Horario", back_populates="actividades")
    respuestas = relationship("RespActividad", back_populates="actividad")

class RespActividad(Base):
    __tablename__ = "resp_actividad"
    id_resp = Column(Integer, primary_key=True, index=True)
    id_inscripcion = Column(Integer, ForeignKey("inscripcion.id_inscripcion"), nullable=False)
    link_repositorio = Column(Text)
    fecha_entrega = Column(Date)
    hora_entrega = Column(Time)
    comentario = Column(Text)

    inscripcion = relationship("Inscripcion", back_populates="respuestas")
    actividad = relationship("ActividadFinal", back_populates="respuestas")