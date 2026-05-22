from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.core.security import get_current_user, require_role
from app.modules.auth.models.usuario import Usuario
from app.modules.courses.schemas.ruta_aprendizaje import RutaAprendizajeCreate, RutaAprendizajeRead, RutaAprendizajeUpdate
from app.modules.courses.services.ruta_aprendizaje_service import crear_ruta, obtener_ruta, listar_rutas, actualizar_ruta, eliminar_ruta

router = APIRouter(prefix="/courses/rutas", tags=["🗺️ Rutas de Aprendizaje"])

@router.post("/", response_model=RutaAprendizajeRead, status_code=status.HTTP_201_CREATED, operation_id="crear_ruta_aprendizaje")
def crear_ruta_aprendizaje(
    data: RutaAprendizajeCreate, 
    db: Session = Depends(get_db), 
    current_user: Usuario = Depends(require_role("superadmin", "COORDINADOR"))
):
    return crear_ruta(db, data)

@router.get("/", response_model=List[RutaAprendizajeRead], operation_id="listar_rutas_aprendizaje")
def listar_rutas_aprendizaje(
    skip: int = Query(0, ge=0), 
    limit: int = Query(20, ge=1, le=100), 
    db: Session = Depends(get_db), 
    current_user: Usuario = Depends(get_current_user)
):
    return listar_rutas(db, skip, limit)

@router.get("/{id_ruta}", response_model=RutaAprendizajeRead, operation_id="obtener_ruta_aprendizaje")
def obtener_ruta_aprendizaje(
    id_ruta: int, 
    db: Session = Depends(get_db), 
    current_user: Usuario = Depends(get_current_user)
):
    res = obtener_ruta(db, id_ruta)
    if not res:
        raise HTTPException(status_code=404, detail="Ruta de aprendizaje no encontrada")
    return res

@router.put("/{id_ruta}", response_model=RutaAprendizajeRead, operation_id="actualizar_ruta_aprendizaje")
def actualizar_ruta_aprendizaje(
    id_ruta: int, 
    data: RutaAprendizajeUpdate, 
    db: Session = Depends(get_db), 
    current_user: Usuario = Depends(require_role("superadmin", "COORDINADOR"))
):
    res = actualizar_ruta(db, id_ruta, data)
    if not res:
        raise HTTPException(status_code=404, detail="Ruta de aprendizaje no encontrada")
    return res

@router.delete("/{id_ruta}", status_code=status.HTTP_204_NO_CONTENT, operation_id="eliminar_ruta_aprendizaje")
def eliminar_ruta_aprendizaje(
    id_ruta: int, 
    db: Session = Depends(get_db), 
    current_user: Usuario = Depends(require_role("superadmin"))
):
    if not eliminar_ruta(db, id_ruta):
        raise HTTPException(status_code=404, detail="Ruta de aprendizaje no encontrada")