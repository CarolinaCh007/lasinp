from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user, require_role
from app.modules.auth.models.usuario import Usuario
from app.modules.academic.schemas.portafolio import PortafolioCreate, PortafolioRead, PortafolioUpdate
from app.modules.academic.services.portafolio_service import (
    crear_portafolio, obtener_portafolio_por_docente, actualizar_portafolio, eliminar_portafolio
)

router = APIRouter(prefix="/academic/portafolios", tags=["💼 Portafolios"])

@router.post("/", response_model=PortafolioRead, status_code=status.HTTP_201_CREATED)
def crear(data: PortafolioCreate, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    # Solo ADMIN o el propio DOCENTE pueden crear
    if current_user.id_usuario != data.id_docente:
        try: require_role("ADMIN")(current_user=current_user, db=db)
        except: raise HTTPException(status_code=403, detail="Permiso denegado")
    return crear_portafolio(db, data)

@router.get("/{id_docente}", response_model=PortafolioRead)
def obtener(id_docente: int, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    res = obtener_portafolio_por_docente(db, id_docente)
    if not res: raise HTTPException(status_code=404, detail="No encontrado")
    return res

@router.put("/{id_docente}", response_model=PortafolioRead)
def actualizar(id_docente: int, data: PortafolioUpdate, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    if current_user.id_usuario != id_docente:
        try: require_role("ADMIN")(current_user=current_user, db=db)
        except: raise HTTPException(status_code=403, detail="Permiso denegado")
    return actualizar_portafolio(db, id_docente, data)

@router.delete("/{id_docente}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar(id_docente: int, db: Session = Depends(get_db), current_user: Usuario = Depends(require_role("ADMIN"))):
    if not eliminar_portafolio(db, id_docente): raise HTTPException(status_code=404, detail="No encontrado")