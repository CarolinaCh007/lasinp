from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.core.security import get_current_user, require_role
from app.modules.auth.models.usuario import Usuario
from app.modules.courses.schemas.ruta_tiene import RutaTieneCreate, RutaTieneRead
from app.modules.courses.services.ruta_tiene_service import (
    crear_ruta_tiene, obtener_ruta_tiene, 
    listar_cursos_por_ruta, listar_rutas_por_curso, 
    eliminar_ruta_tiene
)

router = APIRouter(prefix="/courses/rutas-relacion", tags=["🔗 Rutas-Cursos"])

@router.post("/", response_model=RutaTieneRead, status_code=status.HTTP_201_CREATED, operation_id="crear_ruta_tiene")
def crear(data: RutaTieneCreate, db: Session = Depends(get_db), current_user: Usuario = Depends(require_role("ADMIN", "COORDINADOR"))):
    return crear_ruta_tiene(db, data)

@router.get("/por-ruta/{id_ruta}", response_model=List[RutaTieneRead], operation_id="listar_cursos_por_ruta")
def listar_cursos(id_ruta: int, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    return listar_cursos_por_ruta(db, id_ruta)

@router.get("/por-curso/{id_curso}", response_model=List[RutaTieneRead], operation_id="listar_rutas_por_curso")
def listar_rutas(id_curso: int, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    return listar_rutas_por_curso(db, id_curso)

@router.delete("/{id_ruta}/{id_curso}", status_code=status.HTTP_204_NO_CONTENT, operation_id="eliminar_ruta_tiene")
def eliminar(id_ruta: int, id_curso: int, db: Session = Depends(get_db), current_user: Usuario = Depends(require_role("ADMIN"))):
    if not eliminar_ruta_tiene(db, id_ruta, id_curso):
        raise HTTPException(status_code=404, detail="Relación no encontrada")