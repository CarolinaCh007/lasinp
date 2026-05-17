from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional, List

from app.core.database import get_db
from app.modules.auth.schemas.usuario import UsuarioRead, UsuarioUpdate
from app.modules.auth.services.usuario_service import (
    obtener_usuario_por_ci,
    actualizar_usuario
)
from app.core.security import get_current_user, require_role  # ← Cambiar aquí
from app.modules.auth.models.usuario import Usuario
from sqlalchemy import select

router = APIRouter(prefix="/users", tags=["👥 Usuarios"])

@router.get("/", response_model=List[UsuarioRead])
def listar_usuarios(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    estado: Optional[bool] = None,
    db: Session = Depends(get_db),
    # ✅ Usar require_role en lugar de get_current_admin
    current_user: Usuario = Depends(require_role("ADMIN"))
):
    """
    Listar usuarios con paginación y filtros.
    Solo accesible para usuarios con rol ADMIN.
    """
    query = select(Usuario)
    
    if estado is not None:
        query = query.where(Usuario.estado == estado)
    
    query = query.offset(skip).limit(limit)
    usuarios = db.execute(query).scalars().all()
    
    return usuarios

@router.get("/{id_usuario}", response_model=UsuarioRead)
def obtener_usuario(
    id_usuario: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)  # Cualquier usuario logueado
):
    """
    Obtener detalles de un usuario por ID.
    - ADMIN: puede ver cualquier usuario.
    - Otros: solo pueden verse a sí mismos.
    """
    # Verificar permisos: ADMIN o dueño del recurso
    if current_user.id_usuario != id_usuario:
        # Verificar si es ADMIN usando require_role de forma manual
        from sqlalchemy import select
        from app.modules.auth.models.rol import Rol
        from app.modules.auth.models.instancia import Instancia
        
        query = select(Rol.nombre).join(Instancia).where(Instancia.id_usuario == current_user.id_usuario)
        user_roles = db.execute(query).scalars().all()
        
        if "ADMIN" not in user_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permiso para ver este usuario"
            )
    
    usuario = db.get(Usuario, id_usuario)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    
    return usuario

@router.put("/{id_usuario}", response_model=UsuarioRead)
def actualizar_usuario_endpoint(
    id_usuario: int,
    usuario_update: UsuarioUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Actualizar datos de un usuario.
    - ADMIN: puede editar cualquier usuario.
    - Otros: solo pueden editar su propio perfil.
    """
    # Verificar permisos: ADMIN o dueño del recurso
    if current_user.id_usuario != id_usuario:
        from sqlalchemy import select
        from app.modules.auth.models.rol import Rol
        from app.modules.auth.models.instancia import Instancia
        
        query = select(Rol.nombre).join(Instancia).where(Instancia.id_usuario == current_user.id_usuario)
        user_roles = db.execute(query).scalars().all()
        
        if "ADMIN" not in user_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permiso para editar este usuario"
            )
    
    usuario_actualizado = actualizar_usuario(db, id_usuario, usuario_update.model_dump(exclude_unset=True))
    
    if not usuario_actualizado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    
    return usuario_actualizado