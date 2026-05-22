from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional, List
from sqlalchemy import select

from app.core.database import get_db
from app.core.security import get_current_user, require_role
from app.modules.auth.models.usuario import Usuario
from app.modules.auth.models.rol import Rol
from app.modules.auth.models.instancia import Instancia
from app.modules.auth.schemas.usuario import (
    UsuarioRead, UsuarioUpdate, RolRead,
    AsignarRolRequest, EstadoUpdateRequest
)
from app.modules.auth.services.usuario_service import (
    actualizar_usuario, obtener_roles_usuario,
    asignar_rol_usuario, cambiar_estado_usuario
)

router = APIRouter(prefix="/users", tags=["👥 Gestión de Usuarios"])

# =============================================================================
# 🔹 CRUD BÁSICO DE USUARIOS (CORREGIDO)
# =============================================================================

@router.get("/", response_model=List[UsuarioRead], operation_id="listar_usuarios")
def listar_usuarios(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    estado: Optional[str] = None,  # ✅ Corregido: era bool, ahora str (coincide con BD)
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_role("superadmin"))
):
    query = select(Usuario)
    if estado:
        query = query.where(Usuario.estado == estado)
    return db.execute(query.offset(skip).limit(limit)).scalars().all()

@router.get("/{id_usuario}", response_model=UsuarioRead, operation_id="obtener_usuario")
def obtener_usuario(
    id_usuario: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    # Solo ADMIN o el propio usuario puede ver detalles
    if current_user.id_usuario != id_usuario:
        require_role("superadmin")(current_user=current_user, db=db)
        
    usuario = db.get(Usuario, id_usuario)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

@router.put("/{id_usuario}", response_model=UsuarioRead, operation_id="actualizar_usuario")
def actualizar_usuario_endpoint(
    id_usuario: int,
    data: UsuarioUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    if current_user.id_usuario != id_usuario:
        require_role("superadmin")(current_user=current_user, db=db)
        
    result = actualizar_usuario(db, id_usuario, data.model_dump(exclude_unset=True))
    if not result:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return result

# =============================================================================
# 🔹 GESTIÓN DE ROLES (ADMIN)
# =============================================================================

@router.get("/roles/disponibles", response_model=List[RolRead], operation_id="listar_roles_disponibles")
def listar_roles(db: Session = Depends(get_db), current_user: Usuario = Depends(require_role("superadmin"))):
    """Lista todos los roles existentes en el sistema"""
    return db.execute(select(Rol).order_by(Rol.nombre)).scalars().all()

@router.get("/{id_usuario}/roles", response_model=List[RolRead], operation_id="obtener_roles_usuario")
def obtener_roles_de_usuario(
    id_usuario: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    if current_user.id_usuario != id_usuario:
        require_role("superadmin")(current_user=current_user, db=db)
    return obtener_roles_usuario(db, id_usuario)

@router.post("/{id_usuario}/roles", status_code=status.HTTP_201_CREATED, operation_id="asignar_rol")
def asignar_rol(
    id_usuario: int,
    data: AsignarRolRequest,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_role("superadmin"))
):
    """Asigna un rol a un usuario (ADMIN only)"""
    asignar_rol_usuario(db, id_usuario, data.nombre_rol)
    return {"message": f"Rol '{data.nombre_rol}' asignado exitosamente"}

@router.delete("/{id_usuario}/roles/{nombre_rol}", status_code=status.HTTP_204_NO_CONTENT, operation_id="revocar_rol")
def revocar_rol(
    id_usuario: int,
    nombre_rol: str,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_role("superadmin"))
):
    """Elimina la asignación de un rol a un usuario"""
    rol = db.execute(select(Rol).where(Rol.nombre == nombre_rol)).scalar_one_or_none()
    if not rol:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
        
    instancia = db.execute(
        select(Instancia).where(Instancia.id_usuario == id_usuario, Instancia.id_rol == rol.id_rol)
    ).scalar_one_or_none()
    if not instancia:
        raise HTTPException(status_code=404, detail="El usuario no tiene este rol asignado")
        
    db.delete(instancia)
    db.commit()

# =============================================================================
# 🔹 GESTIÓN DE ESTADOS (ADMIN)
# =============================================================================

@router.patch("/{id_usuario}/estado", response_model=UsuarioRead, operation_id="cambiar_estado_usuario")
def cambiar_estado(
    id_usuario: int,
    data: EstadoUpdateRequest,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_role("superadmin"))
):
    """Cambia el estado de un usuario (activo/inactivo/pendiente/bloqueado)"""
    result = cambiar_estado_usuario(db, id_usuario, data.estado)
    if not result:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return result

@router.post("/{id_usuario}/bloquear", status_code=status.HTTP_200_OK, operation_id="bloquear_usuario")
def bloquear_usuario(
    id_usuario: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_role("superadmin"))
):
    """Atajo para bloquear un usuario inmediatamente"""
    return cambiar_estado(db, id_usuario, EstadoUpdateRequest(estado="bloqueado"))

@router.post("/{id_usuario}/activar", status_code=status.HTTP_200_OK, operation_id="activar_usuario")
def activar_usuario(
    id_usuario: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_role("superadmin"))
):
    """Atajo para activar un usuario inmediatamente"""
    return cambiar_estado(db, id_usuario, EstadoUpdateRequest(estado="activo"))