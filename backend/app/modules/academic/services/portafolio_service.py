from sqlalchemy.orm import Session
from typing import Optional
from fastapi import HTTPException, status

from app.modules.academic.models.docente import Docente
from app.modules.academic.models.portafolio import Portafolio
from app.modules.academic.schemas.portafolio import PortafolioCreate, PortafolioUpdate

def crear_portafolio(db: Session, data: PortafolioCreate) -> Portafolio:
    docente = db.get(Docente, data.id_docente)
    if not docente:
        raise HTTPException(status_code=404, detail="Docente no encontrado")
    if db.query(Portafolio).filter(Portafolio.id_docente == data.id_docente).first():
        raise HTTPException(status_code=400, detail="El docente ya tiene un portafolio")
    
    nuevo = Portafolio(id_docente=data.id_docente, direccion_cv=data.direccion_cv, linkedin=data.linkedin, github=data.github)
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

def obtener_portafolio_por_docente(db: Session, id_docente: int) -> Optional[Portafolio]:
    return db.query(Portafolio).filter(Portafolio.id_docente == id_docente).first()

def actualizar_portafolio(db: Session, id_docente: int, data: PortafolioUpdate) -> Portafolio:
    port = db.query(Portafolio).filter(Portafolio.id_docente == id_docente).first()
    if not port:
        raise HTTPException(status_code=404, detail="Portafolio no encontrado para este docente")
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(port, k, v)
    db.commit()
    db.refresh(port)
    return port

def eliminar_portafolio(db: Session, id_docente: int) -> bool:
    port = db.query(Portafolio).filter(Portafolio.id_docente == id_docente).first()
    if not port: return False
    db.delete(port)
    db.commit()
    return True