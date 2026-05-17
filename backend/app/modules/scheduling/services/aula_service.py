from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import Optional, List
from fastapi import HTTPException, status
from app.modules.scheduling.models.aula import Aula
from app.modules.scheduling.schemas.aula import AulaCreate, AulaUpdate

def crear_aula(db: Session, data: AulaCreate) -> Aula:
    nuevo = Aula(**data.model_dump())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

def obtener_aula(db: Session, id_aula: int) -> Optional[Aula]:
    return db.get(Aula, id_aula)

def listar_aulas(db: Session, skip: int = 0, limit: int = 20) -> List[Aula]:
    stmt = select(Aula).offset(skip).limit(limit)
    return db.execute(stmt).scalars().all()

def actualizar_aula(db: Session, id_aula: int, data: AulaUpdate) -> Optional[Aula]:
    aula = db.get(Aula, id_aula)
    if not aula:
        return None
    for key, value in data.model_dump(exclude_unset=True).items():
        if hasattr(aula, key):
            setattr(aula, key, value)
    db.commit()
    db.refresh(aula)
    return aula

def eliminar_aula(db: Session, id_aula: int) -> bool:
    aula = db.get(Aula, id_aula)
    if not aula:
        return False
    db.delete(aula)
    db.commit()
    return True