from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.core.security import get_current_user, require_role
from app.modules.auth.models.usuario import Usuario
from app.modules.scheduling.schemas.aula import AulaCreate, AulaRead, AulaUpdate
from app.modules.scheduling.services.aula_service import crear_aula, obtener_aula, listar_aulas, actualizar_aula, eliminar_aula

router = APIRouter(prefix="/scheduling/aulas", tags=["🏫 Aulas"])

@router.post("/", response_model=AulaRead, status_code=status.HTTP_201_CREATED, operation_id="crear_aula")
def crear_aula_endpoint(
    data: AulaCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_role("ADMIN", "COORDINADOR"))
):
    return crear_aula(db, data)

@router.get("/", response_model=List[AulaRead], operation_id="listar_aulas")
def listar_aulas_endpoint(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    return listar_aulas(db, skip, limit)

@router.get("/{id_aula}", response_model=AulaRead, operation_id="obtener_aula")
def obtener_aula_endpoint(
    id_aula: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    res = obtener_aula(db, id_aula)
    if not res:
        raise HTTPException(status_code=404, detail="Aula no encontrada")
    return res

@router.put("/{id_aula}", response_model=AulaRead, operation_id="actualizar_aula")
def actualizar_aula_endpoint(
    id_aula: int,
    data: AulaUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_role("ADMIN", "COORDINADOR"))
):
    res = actualizar_aula(db, id_aula, data)
    if not res:
        raise HTTPException(status_code=404, detail="Aula no encontrada")
    return res

@router.delete("/{id_aula}", status_code=status.HTTP_204_NO_CONTENT, operation_id="eliminar_aula")
def eliminar_aula_endpoint(
    id_aula: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_role("ADMIN"))
):
    if not eliminar_aula(db, id_aula):
        raise HTTPException(status_code=404, detail="Aula no encontrada")