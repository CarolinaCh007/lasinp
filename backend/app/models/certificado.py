from sqlalchemy import Column, Integer, String, Date, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Certificado(Base):
    __tablename__ = "certificado"
    id_certificado = Column(Integer, primary_key=True, index=True)
    id_inscripcion = Column(Integer, ForeignKey("inscripcion.id_inscripcion"), unique=True, nullable=False)
    codigo_verificacion = Column(String(100), unique=True, nullable=False)
    fecha_emision = Column(Date)
    qr_url = Column(Text)
    estado = Column(String(20), default="pendiente")
    hash_certificado = Column(Text)
    url_certificado = Column(Text)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    inscripcion = relationship("Inscripcion", back_populates="certificado")