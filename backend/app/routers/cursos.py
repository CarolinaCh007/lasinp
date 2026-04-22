from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.curso import Curso
from app.schemas.curso import CursoCreate, CursoResponse, CursoUpdate
from app.core.dependencies import require_rol
from datetime import datetime

router = APIRouter(prefix="/cursos", tags=["Cursos"])

# ── GET todos los cursos ──────────────────────────────────
@router.get("/", response_model=List[CursoResponse])
def listar_cursos(db: Session = Depends(get_db)):
    return db.query(Curso).all()

# ── GET curso por ID ──────────────────────────────────────
@router.get("/{id_curso}", response_model=CursoResponse)
def obtener_curso(id_curso: int, db: Session = Depends(get_db)):
    curso = db.query(Curso).filter(Curso.id_curso == id_curso).first()
    if not curso:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    return curso

# ── POST crear curso ──────────────────────────────────────
@router.post("/", response_model=CursoResponse, status_code=status.HTTP_201_CREATED)
def crear_curso(
    curso: CursoCreate,
    db: Session = Depends(get_db),
    _=Depends(require_rol("admin", "superadmin"))
):
    # Verificar sigla duplicada
    if curso.sigla and db.query(Curso).filter(Curso.sigla == curso.sigla).first():
        raise HTTPException(status_code=400, detail="La sigla ya está registrada")

    nuevo = Curso(**curso.model_dump())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

# ── PUT actualizar curso ──────────────────────────────────
@router.put("/{id_curso}", response_model=CursoResponse)
def actualizar_curso(
    id_curso: int,
    datos: CursoUpdate,
    db: Session = Depends(get_db),
    _=Depends(require_rol("admin", "superadmin"))
):
    curso = db.query(Curso).filter(Curso.id_curso == id_curso).first()
    if not curso:
        raise HTTPException(status_code=404, detail="Curso no encontrado")

    for campo, valor in datos.model_dump(exclude_unset=True).items():
        setattr(curso, campo, valor)

    curso.updated_at = datetime.now()
    db.commit()
    db.refresh(curso)
    return curso

# ── DELETE eliminar curso ─────────────────────────────────
@router.delete("/{id_curso}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_curso(
    id_curso: int,
    db: Session = Depends(get_db),
    _=Depends(require_rol("superadmin"))
):
    curso = db.query(Curso).filter(Curso.id_curso == id_curso).first()
    if not curso:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    db.delete(curso)
    db.commit()

# ── PATCH cambiar estado ──────────────────────────────────
@router.patch("/{id_curso}/estado", response_model=CursoResponse)
def cambiar_estado(
    id_curso: int,
    estado: str,
    db: Session = Depends(get_db),
    _=Depends(require_rol("admin", "superadmin"))
):
    estados_validos = ["activo", "inactivo", "pendiente", "archivado"]
    if estado not in estados_validos:
        raise HTTPException(status_code=400, detail=f"Estado inválido. Use: {estados_validos}")

    curso = db.query(Curso).filter(Curso.id_curso == id_curso).first()
    if not curso:
        raise HTTPException(status_code=404, detail="Curso no encontrado")

    curso.estado = estado
    curso.updated_at = datetime.now()
    db.commit()
    db.refresh(curso)
    return curso