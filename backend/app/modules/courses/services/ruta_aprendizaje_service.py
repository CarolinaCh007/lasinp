from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import Optional, List
from fastapi import HTTPException, status
from app.modules.courses.models.ruta_aprendizaje import RutaAprendizaje
from app.modules.courses.schemas.ruta_aprendizaje import RutaAprendizajeCreate, RutaAprendizajeUpdate

def crear_ruta(db: Session, data: RutaAprendizajeCreate) -> RutaAprendizaje:
    nuevo = RutaAprendizaje(**data.model_dump())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

def obtener_ruta(db: Session, id_ruta: int) -> Optional[RutaAprendizaje]:
    return db.get(RutaAprendizaje, id_ruta)

def listar_rutas(db: Session, skip: int = 0, limit: int = 20) -> List[RutaAprendizaje]:
    stmt = select(RutaAprendizaje).offset(skip).limit(limit)
    return db.execute(stmt).scalars().all()

def actualizar_ruta(db: Session, id_ruta: int, data: RutaAprendizajeUpdate) -> Optional[RutaAprendizaje]:
    ruta = db.get(RutaAprendizaje, id_ruta)
    if not ruta:
        return None
    for key, value in data.model_dump(exclude_unset=True).items():
        if hasattr(ruta, key):
            setattr(ruta, key, value)
    db.commit()
    db.refresh(ruta)
    return ruta

def eliminar_ruta(db: Session, id_ruta: int) -> bool:
    ruta = db.get(RutaAprendizaje, id_ruta)
    if not ruta:
        return False
    db.delete(ruta)
    db.commit()
    return True