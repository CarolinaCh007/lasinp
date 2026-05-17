from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.core.config import settings
from app.core.database import get_db
from app.modules.auth.models.usuario import Usuario
from app.modules.auth.models.instancia import Instancia
from app.modules.auth.models.rol import Rol
from app.modules.auth.services.auth_service import verificar_password

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

def obtener_usuario_por_id(db: Session, usuario_id: int) -> Optional[Usuario]:
    return db.get(Usuario, usuario_id)

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> Usuario:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciales inválidas",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: Optional[int] = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    usuario = obtener_usuario_por_id(db, int(user_id))
    if usuario is None or not usuario.estado:
        raise credentials_exception
    return usuario

def require_role(*roles: str):
    """Dependency factory: verifica que el usuario tenga AL MENOS UNO de los roles requeridos"""
    async def role_checker(
        current_user: Usuario = Depends(get_current_user),
        db: Session = Depends(get_db)
    ) -> Usuario:
        query = select(Rol.nombre).join(Instancia).where(Instancia.id_usuario == current_user.id_usuario)
        user_roles = db.execute(query).scalars().all()
        
        if not any(r in user_roles for r in roles):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Permiso denegado. Se requiere rol: {', '.join(roles)}"
            )
        return current_user
    return role_checker