from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.core.security import get_current_user, require_role
from app.modules.auth.models.usuario import Usuario
from app.modules.scheduling.schemas.horario import HorarioCreate, HorarioRead, HorarioUpdate
from app.modules.scheduling.services.horario_service import (
    crear_horario, obtener_horario, listar_horarios, actualizar_horario, eliminar_horario
)

router = APIRouter(prefix="/scheduling/horarios", tags=["🗓️ Horarios"])

@router.post("/", response_model=HorarioRead, status_code=status.HTTP_201_CREATED, operation_id="crear_horario")
def crear_horario_endpoint(
    data: HorarioCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_role("ADMIN", "COORDINADOR"))
):
    try:
        return crear_horario(db, data)
    except HTTPException as e:
        raise e

@router.get("/", response_model=List[HorarioRead], operation_id="listar_horarios")
def listar_horarios_endpoint(
    id_curso: Optional[int] = Query(None, ge=1),
    id_aula: Optional[int] = Query(None, ge=1),
    id_docente: Optional[int] = Query(None, ge=1),
    dia_semana: Optional[str] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    return listar_horarios(db, id_curso, id_aula, id_docente, dia_semana, skip, limit)

@router.get("/{id_horario}", response_model=HorarioRead, operation_id="obtener_horario")
def obtener_horario_endpoint(
    id_horario: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    res = obtener_horario(db, id_horario)
    if not res:
        raise HTTPException(status_code=404, detail="Horario no encontrado")
    return res

@router.put("/{id_horario}", response_model=HorarioRead, operation_id="actualizar_horario")
def actualizar_horario_endpoint(
    id_horario: int,
    data: HorarioUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_role("ADMIN", "COORDINADOR"))
):
    try:
        res = actualizar_horario(db, id_horario, data)
        if not res:
            raise HTTPException(status_code=404, detail="Horario no encontrado")
        return res
    except HTTPException as e:
        raise e

@router.delete("/{id_horario}", status_code=status.HTTP_204_NO_CONTENT, operation_id="eliminar_horario")
def eliminar_horario_endpoint(
    id_horario: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_role("ADMIN"))
):
    if not eliminar_horario(db, id_horario):
        raise HTTPException(status_code=404, detail="Horario no encontrado")