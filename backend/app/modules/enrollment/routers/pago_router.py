from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.core.security import get_current_user, require_role
from app.modules.auth.models.usuario import Usuario
from app.modules.enrollment.schemas.pago import PagoCreate, PagoRead, PagoUpdate
from app.modules.enrollment.services.pago_service import crear_pago, obtener_pago, listar_pagos, actualizar_pago, eliminar_pago

router = APIRouter(prefix="/enrollment/pagos", tags=["💰 Pagos"])

@router.post("/", response_model=PagoRead, status_code=status.HTTP_201_CREATED, operation_id="crear_pago")
def crear_pago_endpoint(data: PagoCreate, db: Session = Depends(get_db), current_user: Usuario = Depends(require_role("superadmin", "COORDINADOR"))):
    return crear_pago(db, data)

@router.get("/", response_model=List[PagoRead], operation_id="listar_pagos")
def listar_pagos_endpoint(id_inscripcion: Optional[int] = Query(None, ge=1), skip: int = Query(0, ge=0), limit: int = Query(20, ge=1, le=100), db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    return listar_pagos(db, id_inscripcion, skip, limit)

@router.get("/{id_pago}", response_model=PagoRead, operation_id="obtener_pago")
def obtener_pago_endpoint(id_pago: int, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    res = obtener_pago(db, id_pago)
    if not res: raise HTTPException(status_code=404, detail="Pago no encontrado")
    return res

@router.put("/{id_pago}", response_model=PagoRead, operation_id="actualizar_pago")
def actualizar_pago_endpoint(id_pago: int, data: PagoUpdate, db: Session = Depends(get_db), current_user: Usuario = Depends(require_role("superadmin", "COORDINADOR"))):
    res = actualizar_pago(db, id_pago, data)
    if not res: raise HTTPException(status_code=404, detail="Pago no encontrado")
    return res

@router.delete("/{id_pago}", status_code=status.HTTP_204_NO_CONTENT, operation_id="eliminar_pago")
def eliminar_pago_endpoint(id_pago: int, db: Session = Depends(get_db), current_user: Usuario = Depends(require_role("superadmin"))):
    if not eliminar_pago(db, id_pago): raise HTTPException(status_code=404, detail="Pago no encontrado")

from app.modules.enrollment.services.pago_service import listar_historial_pagos_estudiante

# 🔹 4. Historial de pagos por estudiante
@router.get("/historial/{id_estudiante}", response_model=List[dict], operation_id="historial_pagos_estudiante")
def historial_pagos_estudiante_endpoint(
    id_estudiante: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Historial de pagos de un estudiante.
    - El estudiante solo ve SU historial
    - ADMIN/COORD ve cualquier historial
    """
    if current_user.id_usuario != id_estudiante:
        try: require_role("superadmin", "COORDINADOR")(current_user=current_user, db=db)
        except: raise HTTPException(status_code=403, detail="Solo puedes ver tu propio historial o requerir rol ADMIN.")
    
    return listar_historial_pagos_estudiante(db, id_estudiante)