from sqlalchemy import Column, Integer, Date, Time, String, Numeric, Text, DateTime, ForeignKey, func
from app.core.database import Base

class Pago(Base):
    __tablename__ = "pago"
    __table_args__ = {"extend_existing": True}
    
    id_pago = Column(Integer, primary_key=True, index=True)
    id_inscripcion = Column(Integer, ForeignKey("inscripcion.id_inscripcion", ondelete="RESTRICT"), nullable=False, index=True)
    precio = Column(Numeric(10, 2))
    fecha_pago = Column(Date)
    hora_pago = Column(Time)
    estado = Column(String(20), default="pendiente", server_default="pendiente")
    metodo_pago = Column(String(50))
    id_transaccion_lib = Column(Text)
    codigo_recaudacion = Column(Text)
    observaciones = Column(Text)
    url_pasarela = Column(Text)
    identificador_deuda = Column(Text)
    ci_nit_facturacion = Column(String(20))
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())