from sqlalchemy import Column, Integer, Text, ForeignKey
from app.core.database import Base

class Portafolio(Base):
    __tablename__ = "portafolio"
    __table_args__ = {"extend_existing": True}
    
    id_portafolio = Column(Integer, primary_key=True, index=True)
    id_docente = Column(Integer, ForeignKey("docente.id_docente", ondelete="CASCADE"), unique=True, nullable=False)
    direccion_cv = Column(Text, nullable=True)
    linkedin = Column(Text, nullable=True)
    github = Column(Text, nullable=True)

    # 🔹 SIN relationships → cero conflictos