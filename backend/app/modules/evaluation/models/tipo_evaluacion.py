from sqlalchemy import Column, Integer, String, Numeric, ForeignKey
from app.core.database import Base
class TipoEvaluacion(Base):
    __tablename__ = "tipo_evaluacion"
    __table_args__ = {"extend_existing": True}
    id_tipo = Column(Integer, primary_key=True, index=True)
    id_curso = Column(Integer, ForeignKey("curso.id_curso", ondelete="RESTRICT"), nullable=False)
    nombre = Column(String(100), nullable=False)
    peso_porcentual = Column(Numeric(5, 2))