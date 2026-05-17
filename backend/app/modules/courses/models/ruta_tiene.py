from sqlalchemy import Column, Integer, ForeignKey
from app.core.database import Base

class RutaTiene(Base):
    __tablename__ = "ruta_tiene"
    __table_args__ = {"extend_existing": True}
    id_ruta = Column(Integer, ForeignKey("ruta_aprendizaje.id_ruta", ondelete="RESTRICT"), primary_key=True)
    id_curso = Column(Integer, ForeignKey("curso.id_curso", ondelete="RESTRICT"), primary_key=True)