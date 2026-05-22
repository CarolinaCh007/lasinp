from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.core.security import get_current_user, require_role
from app.modules.auth.models.usuario import Usuario
from app.modules.courses.schemas.tema import TemaCreate, TemaRead, TemaUpdate
from app.modules.courses.services.tema_service import crear_tema, obtener_tema, listar_temas, actualizar_tema, eliminar_tema

router = APIRouter(prefix="/courses/temas", tags=["📑 Temas"])

@router.post("/", response_model=TemaRead, status_code=status.HTTP_201_CREATED, operation_id="crear_tema")
def crear(data: TemaCreate, db: Session = Depends(get_db), current_user: Usuario = Depends(require_role("superadmin", "COORDINADOR"))):
    return crear_tema(db, data)

@router.get("/", response_model=List[TemaRead], operation_id="listar_temas")
def listar(id_curso: Optional[int] = Query(None, ge=1), skip: int = Query(0, ge=0), limit: int = Query(20, ge=1, le=100), db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    return listar_temas(db, id_curso, skip, limit)

@router.get("/{id_tema}", response_model=TemaRead)
def obtener(id_tema: int, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    res = obtener_tema(db, id_tema)
    if not res:
        raise HTTPException(status_code=404, detail="Tema no encontrado")
    return res

@router.put("/{id_tema}", response_model=TemaRead, operation_id="actualizar_tema")
def actualizar(id_tema: int, data: TemaUpdate, db: Session = Depends(get_db), current_user: Usuario = Depends(require_role("superadmin", "COORDINADOR"))):
    res = actualizar_tema(db, id_tema, data)
    if not res:
        raise HTTPException(status_code=404, detail="Tema no encontrado")
    return res

@router.delete("/{id_tema}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar(id_tema: int, db: Session = Depends(get_db), current_user: Usuario = Depends(require_role("superadmin"))):
    if not eliminar_tema(db, id_tema):
        raise HTTPException(status_code=404, detail="Tema no encontrado")