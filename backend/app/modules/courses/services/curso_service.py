from sqlalchemy.orm import Session
from sqlalchemy import select, exc
from typing import Optional, List
from fastapi import HTTPException, status
from app.modules.courses.models.curso import Curso
from app.modules.courses.schemas.curso import CursoCreate, CursoUpdate

def crear_curso(db: Session, data: CursoCreate) -> Curso:
    try:
        nuevo = Curso(**data.model_dump())
        db.add(nuevo); db.commit(); db.refresh(nuevo)
        return nuevo
    except exc.IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="La sigla del curso ya existe.")

def obtener_curso(db: Session, id_curso: int) -> Optional[Curso]:
    return db.get(Curso, id_curso)

def listar_cursos(db: Session, skip: int = 0, limit: int = 20, estado: Optional[str] = None) -> List[Curso]:
    stmt = select(Curso)
    if estado: stmt = stmt.where(Curso.estado == estado)
    return db.execute(stmt.offset(skip).limit(limit)).scalars().all()

def actualizar_curso(db: Session, id_curso: int, data: CursoUpdate) -> Optional[Curso]:
    curso = db.get(Curso, id_curso)
    if not curso: return None
    for k, v in data.model_dump(exclude_unset=True).items(): setattr(curso, k, v)
    try: db.commit(); db.refresh(curso); return curso
    except exc.IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="La sigla del curso ya existe.")

def eliminar_curso(db: Session, id_curso: int) -> bool:
    curso = db.get(Curso, id_curso)
    if not curso: return False
    db.delete(curso); db.commit(); return True