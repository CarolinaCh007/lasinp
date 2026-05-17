from sqlalchemy.orm import Session
from sqlalchemy import select, exc
from typing import Optional, List
from fastapi import HTTPException, status
from app.modules.courses.models.ruta_tiene import RutaTiene
from app.modules.courses.schemas.ruta_tiene import RutaTieneCreate

def crear_ruta_tiene(db: Session, data: RutaTieneCreate) -> RutaTiene:
    try:
        # Verificar que la relación no exista ya
        existing = db.query(RutaTiene).filter(
            RutaTiene.id_ruta == data.id_ruta,
            RutaTiene.id_curso == data.id_curso
        ).first()
        if existing:
            raise HTTPException(status_code=400, detail="Esta ruta ya incluye este curso.")
        
        nuevo = RutaTiene(**data.model_dump())
        db.add(nuevo)
        db.commit()
        db.refresh(nuevo)
        return nuevo
    except exc.IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Error: verifica que id_ruta e id_curso existan.")

def obtener_ruta_tiene(db: Session, id_ruta: int, id_curso: int) -> Optional[RutaTiene]:
    return db.query(RutaTiene).filter(
        RutaTiene.id_ruta == id_ruta,
        RutaTiene.id_curso == id_curso
    ).first()

def listar_cursos_por_ruta(db: Session, id_ruta: int) -> List[RutaTiene]:
    stmt = select(RutaTiene).where(RutaTiene.id_ruta == id_ruta)
    return db.execute(stmt).scalars().all()

def listar_rutas_por_curso(db: Session, id_curso: int) -> List[RutaTiene]:
    stmt = select(RutaTiene).where(RutaTiene.id_curso == id_curso)
    return db.execute(stmt).scalars().all()

def eliminar_ruta_tiene(db: Session, id_ruta: int, id_curso: int) -> bool:
    relacion = db.query(RutaTiene).filter(
        RutaTiene.id_ruta == id_ruta,
        RutaTiene.id_curso == id_curso
    ).first()
    if not relacion:
        return False
    db.delete(relacion)
    db.commit()
    return True