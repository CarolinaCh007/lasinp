from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.models.inscripcion import Calificacion, TipoEvaluacion, Inscripcion
from app.core.dependencies import require_rol
from pydantic import BaseModel
from datetime import datetime
from decimal import Decimal

router = APIRouter(prefix="/calificaciones", tags=["Calificaciones"])

# ── Schemas inline ────────────────────────────────────────
class TipoEvaluacionCreate(BaseModel):
    id_curso: int
    nombre: str
    peso_porcentual: Optional[Decimal] = None

class TipoEvaluacionResponse(BaseModel):
    id_tipo: int
    id_curso: int
    nombre: str
    peso_porcentual: Optional[Decimal] = None

    class Config:
        from_attributes = True

class CalificacionCreate(BaseModel):
    id_inscripcion: int
    id_tipo: int
    puntaje: Decimal

class CalificacionUpdate(BaseModel):
    puntaje: Optional[Decimal] = None

class CalificacionResponse(BaseModel):
    id_nota: int
    id_inscripcion: int
    id_tipo: int
    puntaje: Optional[Decimal] = None
    fecha_registro: Optional[datetime] = None

    class Config:
        from_attributes = True

# ══════════════════════════════════════════════════════════
# TIPOS DE EVALUACION
# ══════════════════════════════════════════════════════════

# ── GET tipos por curso ───────────────────────────────────
@router.get("/tipos/curso/{id_curso}", response_model=List[TipoEvaluacionResponse])
def tipos_por_curso(
    id_curso: int,
    db: Session = Depends(get_db),
    _=Depends(require_rol("admin", "superadmin", "docente"))
):
    return db.query(TipoEvaluacion).filter(TipoEvaluacion.id_curso == id_curso).all()

# ── POST crear tipo evaluacion ────────────────────────────
@router.post("/tipos", response_model=TipoEvaluacionResponse, status_code=status.HTTP_201_CREATED)
def crear_tipo_evaluacion(
    tipo: TipoEvaluacionCreate,
    db: Session = Depends(get_db),
    _=Depends(require_rol("admin", "superadmin", "docente"))
):
    nuevo = TipoEvaluacion(**tipo.model_dump())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

# ── DELETE tipo evaluacion ────────────────────────────────
@router.delete("/tipos/{id_tipo}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_tipo_evaluacion(
    id_tipo: int,
    db: Session = Depends(get_db),
    _=Depends(require_rol("admin", "superadmin"))
):
    tipo = db.query(TipoEvaluacion).filter(TipoEvaluacion.id_tipo == id_tipo).first()
    if not tipo:
        raise HTTPException(status_code=404, detail="Tipo de evaluación no encontrado")
    db.delete(tipo)
    db.commit()

# ══════════════════════════════════════════════════════════
# CALIFICACIONES
# ══════════════════════════════════════════════════════════

# ── GET calificaciones por inscripcion ────────────────────
@router.get("/inscripcion/{id_inscripcion}", response_model=List[CalificacionResponse])
def calificaciones_por_inscripcion(
    id_inscripcion: int,
    db: Session = Depends(get_db),
    _=Depends(require_rol("admin", "superadmin", "docente", "estudiante"))
):
    return db.query(Calificacion).filter(
        Calificacion.id_inscripcion == id_inscripcion
    ).all()

# ── POST registrar calificacion ───────────────────────────
@router.post("/", response_model=CalificacionResponse, status_code=status.HTTP_201_CREATED)
def registrar_calificacion(
    calificacion: CalificacionCreate,
    db: Session = Depends(get_db),
    _=Depends(require_rol("admin", "superadmin", "docente"))
):
    # Verificar inscripcion existe
    inscripcion = db.query(Inscripcion).filter(
        Inscripcion.id_inscripcion == calificacion.id_inscripcion
    ).first()
    if not inscripcion:
        raise HTTPException(status_code=404, detail="Inscripcion no encontrada")

    # Verificar tipo evaluacion existe
    tipo = db.query(TipoEvaluacion).filter(
        TipoEvaluacion.id_tipo == calificacion.id_tipo
    ).first()
    if not tipo:
        raise HTTPException(status_code=404, detail="Tipo de evaluación no encontrado")

    # Verificar calificacion duplicada
    existe = db.query(Calificacion).filter(
        Calificacion.id_inscripcion == calificacion.id_inscripcion,
        Calificacion.id_tipo == calificacion.id_tipo
    ).first()
    if existe:
        raise HTTPException(status_code=400, detail="Ya existe calificación para este tipo de evaluación")

    nueva = Calificacion(**calificacion.model_dump())
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva

# ── PUT actualizar calificacion ───────────────────────────
@router.put("/{id_nota}", response_model=CalificacionResponse)
def actualizar_calificacion(
    id_nota: int,
    datos: CalificacionUpdate,
    db: Session = Depends(get_db),
    _=Depends(require_rol("admin", "superadmin", "docente"))
):
    calificacion = db.query(Calificacion).filter(
        Calificacion.id_nota == id_nota
    ).first()
    if not calificacion:
        raise HTTPException(status_code=404, detail="Calificación no encontrada")

    for campo, valor in datos.model_dump(exclude_unset=True).items():
        setattr(calificacion, campo, valor)

    calificacion.fecha_registro = datetime.now()
    db.commit()
    db.refresh(calificacion)
    return calificacion

# ── DELETE calificacion ───────────────────────────────────
@router.delete("/{id_nota}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_calificacion(
    id_nota: int,
    db: Session = Depends(get_db),
    _=Depends(require_rol("admin", "superadmin", "docente"))
):
    calificacion = db.query(Calificacion).filter(
        Calificacion.id_nota == id_nota
    ).first()
    if not calificacion:
        raise HTTPException(status_code=404, detail="Calificación no encontrada")
    db.delete(calificacion)
    db.commit()