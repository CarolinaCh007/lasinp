from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.core.security import get_current_user, require_role
from app.modules.auth.models.usuario import Usuario
from app.modules.academic.schemas.docente import DocenteCreate, DocenteRead, DocenteUpdate
from app.modules.academic.schemas.portafolio import PortafolioCreate, PortafolioRead, PortafolioUpdate
from app.modules.academic.services.docente_service import (
    crear_docente, obtener_docente, listar_docentes,
    actualizar_docente, eliminar_docente
)
from app.modules.academic.services.portafolio_service import (
    crear_portafolio, obtener_portafolio_por_docente, actualizar_portafolio, eliminar_portafolio
)

router = APIRouter(prefix="/academic/docentes", tags=["👨‍🏫 Docentes"])

def _verificar_permiso_docente(current_user: Usuario, target_id: int, db: Session, requerir_admin: bool = False) -> bool:
    """Verifica permisos para operaciones en perfiles de docente"""
    if requerir_admin:
        try:
            require_role("superadmin")(current_user=current_user, db=db)
            return True
        except:
            raise HTTPException(status_code=403, detail="Permiso denegado. Se requiere rol ADMIN.")
    
    if current_user.id_usuario == target_id:
        return True
    
    try:
        require_role("superadmin")(current_user=current_user, db=db)
        return True
    except:
        raise HTTPException(status_code=403, detail="Permiso denegado. Solo puedes editar tu propio perfil.")

# 🔹 Endpoints para DOCENTE (perfil profesional)
@router.post("/", response_model=DocenteRead, status_code=status.HTTP_201_CREATED)
def crear_docente_endpoint(
    data: DocenteCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Crear perfil de docente (propio o por ADMIN)"""
    _verificar_permiso_docente(current_user, data.id_usuario, db)
    
    try:
        doc = crear_docente(db, data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return doc

@router.get("/", response_model=List[DocenteRead])
def listar_docentes_endpoint(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_role("superadmin", "COORDINADOR"))
):
    """Listar docentes (solo ADMIN/COORDINADOR)"""
    return listar_docentes(db, skip, limit)

@router.get("/{id_usuario}", response_model=DocenteRead)
def obtener_docente_endpoint(
    id_usuario: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Obtener perfil de docente (propio o ADMIN/COORDINADOR)"""
    _verificar_permiso_docente(current_user, id_usuario, db)
    
    res = obtener_docente(db, id_usuario)
    if not res:
        raise HTTPException(status_code=404, detail="Perfil de docente no encontrado")
    return res

@router.put("/{id_usuario}", response_model=DocenteRead)
def actualizar_docente_endpoint(
    id_usuario: int,
    data: DocenteUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Actualizar perfil de docente (propio o ADMIN)"""
    _verificar_permiso_docente(current_user, id_usuario, db)
    
    res = actualizar_docente(db, id_usuario, data)
    if not res:
        raise HTTPException(status_code=404, detail="Perfil de docente no encontrado")
    return res

@router.delete("/{id_usuario}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_docente_endpoint(
    id_usuario: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_role("superadmin"))
):
    """Eliminar perfil de docente (solo ADMIN)"""
    if not eliminar_docente(db, id_usuario):
        raise HTTPException(status_code=404, detail="Perfil de docente no encontrado")

# 🔹 Endpoints para PORTAFOLIO (vinculado a docente)
@router.post("/portafolio", response_model=PortafolioRead, status_code=status.HTTP_201_CREATED)
def crear_portafolio_endpoint(
    data: PortafolioCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Crear portafolio (propio docente o ADMIN)"""
    _verificar_permiso_docente(current_user, data.id_docente, db)
    
    try:
        port = crear_portafolio(db, data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return port

@router.get("/portafolio/{id_docente}", response_model=PortafolioRead)
def obtener_portafolio_endpoint(
    id_docente: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Obtener portafolio (público o propio)"""
    # Portafolio puede ser público, pero para edición requiere permiso
    res = obtener_portafolio_por_docente(db, id_docente)
    if not res:
        raise HTTPException(status_code=404, detail="Portafolio no encontrado")
    return res

@router.put("/portafolio/{id_docente}", response_model=PortafolioRead)
def actualizar_portafolio_endpoint(
    id_docente: int,
    data: PortafolioUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Actualizar portafolio (propio docente o ADMIN)"""
    _verificar_permiso_docente(current_user, id_docente, db)
    
    return actualizar_portafolio(db, id_docente, data)

@router.delete("/portafolio/{id_docente}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_portafolio_endpoint(
    id_docente: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_role("superadmin"))
):
    """Eliminar portafolio (solo ADMIN)"""
    if not eliminar_portafolio(db, id_docente):
        raise HTTPException(status_code=404, detail="Portafolio no encontrado")