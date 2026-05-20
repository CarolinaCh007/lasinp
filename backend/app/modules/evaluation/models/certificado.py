from sqlalchemy import Column, Integer, String, Text, Date, DateTime, ForeignKey, func
from app.core.database import Base
class Certificado(Base):
    __tablename__ = "certificado"
    __table_args__ = {"extend_existing": True}
    id_certificado = Column(Integer, primary_key=True, index=True)
    id_inscripcion = Column(Integer, ForeignKey("inscripcion.id_inscripcion", ondelete="RESTRICT"), unique=True, nullable=False)
    codigo_verificacion = Column(String(100), unique=True, nullable=False)
    fecha_emision = Column(Date, server_default=func.current_date())
    qr_url = Column(Text)
    estado = Column(String(20))
    hash_certificado = Column(Text)
    url_certificado = Column(Text)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())