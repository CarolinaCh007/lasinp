from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.core.security import get_current_user, require_role
from app.modules.auth.models.usuario import Usuario
from app.modules.enrollment.schemas.inscripcion import InscripcionCreate, InscripcionRead, InscripcionUpdate
from app.modules.enrollment.services.inscripcion_service import crear_inscripcion, obtener_inscripcion, listar_inscripciones, actualizar_inscripcion, eliminar_inscripcion

router = APIRouter(prefix="/enrollment/inscripciones", tags=["📝 Inscripciones"])

@router.post("/", response_model=InscripcionRead, status_code=status.HTTP_201_CREATED, operation_id="crear_inscripcion")
def crear_inscripcion_endpoint(data: InscripcionCreate, db: Session = Depends(get_db), current_user: Usuario = Depends(require_role("superadmin", "COORDINADOR"))):
    return crear_inscripcion(db, data)

@router.get("/", response_model=List[InscripcionRead], operation_id="listar_inscripciones")
def listar_inscripciones_endpoint(id_estudiante: Optional[int] = Query(None, ge=1), id_horario: Optional[int] = Query(None, ge=1), skip: int = Query(0, ge=0), limit: int = Query(20, ge=1, le=100), db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    return listar_inscripciones(db, id_estudiante, id_horario, skip, limit)

@router.get("/{id_inscripcion}", response_model=InscripcionRead, operation_id="obtener_inscripcion")
def obtener_inscripcion_endpoint(id_inscripcion: int, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    res = obtener_inscripcion(db, id_inscripcion)
    if not res: raise HTTPException(status_code=404, detail="Inscripción no encontrada")
    return res

@router.put("/{id_inscripcion}", response_model=InscripcionRead, operation_id="actualizar_inscripcion")
def actualizar_inscripcion_endpoint(id_inscripcion: int, data: InscripcionUpdate, db: Session = Depends(get_db), current_user: Usuario = Depends(require_role("superadmin", "COORDINADOR"))):
    res = actualizar_inscripcion(db, id_inscripcion, data)
    if not res: raise HTTPException(status_code=404, detail="Inscripción no encontrada")
    return res

@router.delete("/{id_inscripcion}", status_code=status.HTTP_204_NO_CONTENT, operation_id="eliminar_inscripcion")
def eliminar_inscripcion_endpoint(id_inscripcion: int, db: Session = Depends(get_db), current_user: Usuario = Depends(require_role("superadmin"))):
    eliminar_inscripcion(db, id_inscripcion)


from app.modules.enrollment.schemas.inscripcion import InscripcionConPagoRequest
from app.modules.enrollment.services.inscripcion_service import (
    crear_inscripcion_con_pago, listar_inscritos_por_curso, actualizar_estado_inscripcion
)

# 🔹 1. Inscribirse + Subir comprobante (1er pago)
@router.post("/con-pago", response_model=dict, status_code=status.HTTP_201_CREATED, operation_id="crear_inscripcion_con_pago")
def crear_inscripcion_con_pago_endpoint(
    data: InscripcionConPagoRequest,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    El estudiante se inscribe y sube comprobante de pago inicial.
    - Estado inicial: pendiente (hasta que ADMIN/COORD valide el comprobante)
    - Solo el propio estudiante o ADMIN pueden ejecutarlo
    """
    if current_user.id_usuario != data.inscripcion.id_estudiante:
        try: require_role("superadmin")(current_user=current_user, db=db)
        except: raise HTTPException(status_code=403, detail="Solo puedes inscribirte a ti mismo o requerir rol ADMIN.")
    
    return crear_inscripcion_con_pago(db, data)

# 🔹 2. Ver inscritos por curso
@router.get("/por-curso/{id_curso}", response_model=List[dict], operation_id="listar_inscritos_por_curso")
def listar_inscritos_por_curso_endpoint(
    id_curso: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_role("superadmin", "COORDINADOR"))
):
    """Lista de estudiantes inscritos a un curso específico (solo ADMIN/COORD)"""
    return listar_inscritos_por_curso(db, id_curso)

# 🔹 3. Modificar estado de inscripción (validar comprobante)
@router.patch("/{id_inscripcion}/estado", response_model=InscripcionRead, operation_id="actualizar_estado_inscripcion")
def actualizar_estado_inscripcion_endpoint(
    id_inscripcion: int,
    nuevo_estado: str = Query(..., description="activo | inactivo | pendiente | retirado"),
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_role("superadmin", "COORDINADOR"))
):
    """
    Aprueba/rechaza inscripción tras verificar comprobante.
    - Si estado = 'activo', el estudiante queda matriculado oficialmente.
    """
    res = actualizar_estado_inscripcion(db, id_inscripcion, nuevo_estado)
    if not res: raise HTTPException(status_code=404, detail="Inscripción no encontrada")
    return res