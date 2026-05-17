from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.core.security import get_current_user, require_role
from app.modules.auth.models.usuario import Usuario
from app.modules.academic.schemas.estudiante import EstudianteCreate, EstudianteRead, EstudianteUpdate
from app.modules.academic.services.estudiante_service import (
    crear_estudiante, obtener_estudiante, listar_estudiantes,
    actualizar_estudiante, eliminar_estudiante
)

router = APIRouter(prefix="/academic/estudiantes", tags=["🎓 Estudiantes"])

def _verificar_permiso_estudiante(current_user: Usuario, target_id: int, db: Session, requerir_admin: bool = False) -> bool:
    """
    Verifica permisos para operaciones en perfiles de estudiante.
    
    Args:
        current_user: Usuario autenticado
        target_id: ID del usuario objetivo (id_usuario)
        db: Sesión de base de datos
        requerir_admin: Si True, solo ADMIN puede operar
    
    Returns:
        True si tiene permiso, lanza HTTPException si no.
    """
    # Si requiere admin, verificar rol
    if requerir_admin:
        try:
            require_role("ADMIN")(current_user=current_user, db=db)
            return True
        except:
            raise HTTPException(status_code=403, detail="Permiso denegado. Se requiere rol ADMIN.")
    
    # Si no requiere admin: el usuario puede operar sobre sí mismo
    if current_user.id_usuario == target_id:
        return True
    
    # O si es ADMIN, también puede
    try:
        require_role("ADMIN")(current_user=current_user, db=db)
        return True
    except:
        raise HTTPException(status_code=403, detail="Permiso denegado. Solo puedes editar tu propio perfil.")

@router.post("/", response_model=EstudianteRead, status_code=status.HTTP_201_CREATED)
def crear_estudiante_endpoint(
    data: EstudianteCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Crear perfil de estudiante.
    - El usuario puede crear SU PROPIO perfil (id_usuario == current_user.id_usuario)
    - ADMIN puede crear perfil para cualquier usuario
    """
    # Verificar permiso: propio o admin
    _verificar_permiso_estudiante(current_user, data.id_usuario, db)
    
    try:
        est = crear_estudiante(db, data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return est

@router.get("/", response_model=List[EstudianteRead])
def listar_estudiantes_endpoint(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_role("ADMIN", "COORDINADOR"))
):
    """Listar estudiantes (solo ADMIN/COORDINADOR)"""
    return listar_estudiantes(db, skip, limit)

@router.get("/{id_usuario}", response_model=EstudianteRead)
def obtener_estudiante_endpoint(
    id_usuario: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Obtener perfil de estudiante.
    - El usuario puede ver SU PROPIO perfil
    - ADMIN/COORDINADOR puede ver cualquier perfil
    """
    _verificar_permiso_estudiante(current_user, id_usuario, db)
    
    res = obtener_estudiante(db, id_usuario)
    if not res:
        raise HTTPException(status_code=404, detail="Perfil de estudiante no encontrado")
    return res

@router.put("/{id_usuario}", response_model=EstudianteRead)
def actualizar_estudiante_endpoint(
    id_usuario: int,
    data: EstudianteUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Actualizar perfil de estudiante.
    - El usuario puede actualizar SU PROPIO perfil
    - ADMIN puede actualizar cualquier perfil
    """
    _verificar_permiso_estudiante(current_user, id_usuario, db)
    
    res = actualizar_estudiante(db, id_usuario, data)
    if not res:
        raise HTTPException(status_code=404, detail="Perfil de estudiante no encontrado")
    return res

@router.delete("/{id_usuario}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_estudiante_endpoint(
    id_usuario: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_role("ADMIN"))
):
    """Eliminar perfil de estudiante (solo ADMIN)"""
    if not eliminar_estudiante(db, id_usuario):
        raise HTTPException(status_code=404, detail="Perfil de estudiante no encontrado")