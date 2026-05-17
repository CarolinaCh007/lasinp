from sqlalchemy.orm import Session
from sqlalchemy import select, exc
from typing import Optional, List
from fastapi import HTTPException, status
from app.modules.courses.models.tema import Tema
from app.modules.courses.schemas.tema import TemaCreate, TemaUpdate

def crear_tema(db: Session, data: TemaCreate) -> Tema:
    try:
        nuevo = Tema(**data.model_dump())
        db.add(nuevo)
        db.commit()
        db.refresh(nuevo)
        return nuevo
    except exc.IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Error de integridad: verifica id_curso y numero_tema.")

def obtener_tema(db: Session, id_tema: int) -> Optional[Tema]:
    return db.get(Tema, id_tema)

def listar_temas(db: Session, id_curso: Optional[int] = None, skip: int = 0, limit: int = 20) -> List[Tema]:
    stmt = select(Tema)
    if id_curso:
        stmt = stmt.where(Tema.id_curso == id_curso)
    return db.execute(stmt.order_by(Tema.numero_tema).offset(skip).limit(limit)).scalars().all()

def actualizar_tema(db: Session, id_tema: int, data: TemaUpdate) -> Optional[Tema]:
    tema = db.get(Tema, id_tema)
    if not tema:
        return None
    for key, value in data.model_dump(exclude_unset=True).items():
        if hasattr(tema, key):
            setattr(tema, key, value)
    try:
        db.commit()
        db.refresh(tema)
        return tema
    except exc.IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Error de integridad al actualizar.")

def eliminar_tema(db: Session, id_tema: int) -> bool:
    tema = db.get(Tema, id_tema)
    if not tema:
        return False
    db.delete(tema)
    db.commit()
    return True