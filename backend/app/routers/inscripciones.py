from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.inscripcion import Inscripcion, Pago
from app.models.curso import Horario
from app.models.estudiante import Estudiante
from app.schemas.inscripcion import (
    InscripcionCreate, InscripcionResponse, InscripcionUpdate,
    PagoCreate, PagoResponse, PagoUpdate
)
from app.core.dependencies import require_rol, get_current_user
from app.models.usuario import Usuario
from datetime import datetime, date, time as time_type

router = APIRouter(prefix="/inscripciones", tags=["Inscripciones"])

# ── GET todas las inscripciones ───────────────────────────
@router.get("/", response_model=List[InscripcionResponse])
def listar_inscripciones(
    db: Session = Depends(get_db),
    _=Depends(require_rol("admin", "superadmin"))
):
    return db.query(Inscripcion).all()

# ── GET inscripciones por estudiante ──────────────────────
@router.get("/estudiante/{id_estudiante}", response_model=List[InscripcionResponse])
def inscripciones_por_estudiante(
    id_estudiante: int,
    db: Session = Depends(get_db),
    _=Depends(require_rol("admin", "superadmin", "estudiante", "docente"))
):
    return db.query(Inscripcion).filter(
        Inscripcion.id_estudiante == id_estudiante
    ).all()

# ── GET inscripciones por horario ─────────────────────────
@router.get("/horario/{id_horario}", response_model=List[InscripcionResponse])
def inscripciones_por_horario(
    id_horario: int,
    db: Session = Depends(get_db),
    _=Depends(require_rol("admin", "superadmin", "docente"))
):
    return db.query(Inscripcion).filter(
        Inscripcion.id_horario == id_horario
    ).all()

# ── GET inscripcion por ID ────────────────────────────────
@router.get("/{id_inscripcion}", response_model=InscripcionResponse)
def obtener_inscripcion(
    id_inscripcion: int,
    db: Session = Depends(get_db),
    _=Depends(require_rol("admin", "superadmin", "estudiante", "docente"))
):
    inscripcion = db.query(Inscripcion).filter(
        Inscripcion.id_inscripcion == id_inscripcion
    ).first()
    if not inscripcion:
        raise HTTPException(status_code=404, detail="Inscripcion no encontrada")
    return inscripcion

# ── POST crear inscripcion ────────────────────────────────
@router.post("/", response_model=InscripcionResponse, status_code=status.HTTP_201_CREATED)
def crear_inscripcion(
    inscripcion: InscripcionCreate,
    db: Session = Depends(get_db),
    _=Depends(require_rol("admin", "superadmin"))
):
    # Verificar que el horario existe
    horario = db.query(Horario).filter(
        Horario.id_horario == inscripcion.id_horario
    ).first()
    if not horario:
        raise HTTPException(status_code=404, detail="Horario no encontrado")

    # Verificar que el estudiante existe
    estudiante = db.query(Estudiante).filter(
        Estudiante.id_estudiante == inscripcion.id_estudiante
    ).first()
    if not estudiante:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")

    # Verificar inscripcion duplicada
    existe = db.query(Inscripcion).filter(
        Inscripcion.id_horario == inscripcion.id_horario,
        Inscripcion.id_estudiante == inscripcion.id_estudiante
    ).first()
    if existe:
        raise HTTPException(status_code=400, detail="El estudiante ya está inscrito en este horario")

    nueva = Inscripcion(
        id_horario=inscripcion.id_horario,
        id_estudiante=inscripcion.id_estudiante,
        fecha_inscripcion=date.today(),
        hora_inscripcion=datetime.now().time(),
        estado="pendiente"
    )
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva

# ── PUT actualizar inscripcion ────────────────────────────
@router.put("/{id_inscripcion}", response_model=InscripcionResponse)
def actualizar_inscripcion(
    id_inscripcion: int,
    datos: InscripcionUpdate,
    db: Session = Depends(get_db),
    _=Depends(require_rol("admin", "superadmin"))
):
    inscripcion = db.query(Inscripcion).filter(
        Inscripcion.id_inscripcion == id_inscripcion
    ).first()
    if not inscripcion:
        raise HTTPException(status_code=404, detail="Inscripcion no encontrada")

    for campo, valor in datos.model_dump(exclude_unset=True).items():
        setattr(inscripcion, campo, valor)

    inscripcion.updated_at = datetime.now()
    db.commit()
    db.refresh(inscripcion)
    return inscripcion

# ── DELETE eliminar inscripcion ───────────────────────────
@router.delete("/{id_inscripcion}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_inscripcion(
    id_inscripcion: int,
    db: Session = Depends(get_db),
    _=Depends(require_rol("admin", "superadmin"))
):
    inscripcion = db.query(Inscripcion).filter(
        Inscripcion.id_inscripcion == id_inscripcion
    ).first()
    if not inscripcion:
        raise HTTPException(status_code=404, detail="Inscripcion no encontrada")
    db.delete(inscripcion)
    db.commit()

# ══════════════════════════════════════════════════════════
# PAGOS
# ══════════════════════════════════════════════════════════

# ── GET pagos por inscripcion ─────────────────────────────
@router.get("/{id_inscripcion}/pagos", response_model=List[PagoResponse])
def pagos_por_inscripcion(
    id_inscripcion: int,
    db: Session = Depends(get_db),
    _=Depends(require_rol("admin", "superadmin", "estudiante"))
):
    return db.query(Pago).filter(Pago.id_inscripcion == id_inscripcion).all()

# ── POST crear pago ───────────────────────────────────────
@router.post("/{id_inscripcion}/pagos", response_model=PagoResponse, status_code=status.HTTP_201_CREATED)
def crear_pago(
    id_inscripcion: int,
    pago: PagoCreate,
    db: Session = Depends(get_db),
    _=Depends(require_rol("admin", "superadmin"))
):
    inscripcion = db.query(Inscripcion).filter(
        Inscripcion.id_inscripcion == id_inscripcion
    ).first()
    if not inscripcion:
        raise HTTPException(status_code=404, detail="Inscripcion no encontrada")

    nuevo_pago = Pago(
        id_inscripcion=id_inscripcion,
        precio=pago.precio,
        metodo_pago=pago.metodo_pago,
        identificador_deuda=pago.identificador_deuda,
        ci_nit_facturacion=pago.ci_nit_facturacion,
        estado="pendiente",
        fecha_pago=date.today(),
        hora_pago=datetime.now().time()
    )
    db.add(nuevo_pago)
    db.commit()
    db.refresh(nuevo_pago)
    return nuevo_pago

# ── PATCH actualizar estado pago ──────────────────────────
@router.patch("/pagos/{id_pago}/estado", response_model=PagoResponse)
def actualizar_estado_pago(
    id_pago: int,
    estado: str,
    db: Session = Depends(get_db),
    _=Depends(require_rol("admin", "superadmin"))
):
    estados_validos = ["pagado", "pendiente", "no realizado"]
    if estado not in estados_validos:
        raise HTTPException(status_code=400, detail=f"Estado inválido. Use: {estados_validos}")

    pago = db.query(Pago).filter(Pago.id_pago == id_pago).first()
    if not pago:
        raise HTTPException(status_code=404, detail="Pago no encontrado")

    pago.estado = estado
    pago.updated_at = datetime.now()
    db.commit()
    db.refresh(pago)
    return pago