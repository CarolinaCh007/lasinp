from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.core.security import get_current_user, require_role
from app.modules.auth.models.usuario import Usuario
from app.modules.courses.schemas.curso import CursoCreate, CursoRead, CursoUpdate
from app.modules.courses.services.curso_service import crear_curso, obtener_curso, listar_cursos, actualizar_curso, eliminar_curso

router = APIRouter(prefix="/courses/cursos", tags=["📚 Cursos"])

@router.post("/", response_model=CursoRead, status_code=status.HTTP_201_CREATED, operation_id="crear_curso")
def crear(data: CursoCreate, db: Session = Depends(get_db), current_user: Usuario = Depends(require_role("superadmin", "COORDINADOR"))):
    return crear_curso(db, data)

@router.get("/", response_model=List[CursoRead], operation_id="listar_cursos")
def listar(skip: int = Query(0, ge=0), limit: int = Query(20, ge=1, le=100), estado: Optional[str] = None, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    return listar_cursos(db, skip, limit, estado)

@router.get("/{id_curso}", response_model=CursoRead, operation_id="obtener_curso")
def obtener(id_curso: int, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    res = obtener_curso(db, id_curso)
    if not res: raise HTTPException(status_code=404, detail="Curso no encontrado")
    return res

@router.put("/{id_curso}", response_model=CursoRead)
def actualizar(id_curso: int, data: CursoUpdate, db: Session = Depends(get_db), current_user: Usuario = Depends(require_role("superadmin", "COORDINADOR"))):
    res = actualizar_curso(db, id_curso, data)
    if not res: raise HTTPException(status_code=404, detail="Curso no encontrado")
    return res

@router.delete("/{id_curso}", status_code=status.HTTP_204_NO_CONTENT, operation_id="eliminar_curso")
def eliminar(id_curso: int, db: Session = Depends(get_db), current_user: Usuario = Depends(require_role("superadmin"))):
    if not eliminar_curso(db, id_curso): raise HTTPException(status_code=404, detail="Curso no encontrado")