from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.models.inscripcion import Asistencia, Inscripcion
from app.core.dependencies import require_rol
from pydantic import BaseModel
from datetime import date, datetime

router = APIRouter(prefix="/asistencias", tags=["Asistencias"])

# ── Schemas inline ────────────────────────────────────────
class AsistenciaCreate(BaseModel):
    id_inscripcion: int
    fecha_asistencia: date
    estado: str
    observaciones: Optional[str] = None

class AsistenciaUpdate(BaseModel):
    estado: Optional[str] = None
    observaciones: Optional[str] = None

class AsistenciaResponse(BaseModel):
    id_asistencia: int
    id_inscripcion: int
    fecha_asistencia: date
    estado: Optional[str] = None
    observaciones: Optional[str] = None

    class Config:
        from_attributes = True

# ── GET asistencias por inscripcion ───────────────────────
@router.get("/inscripcion/{id_inscripcion}", response_model=List[AsistenciaResponse])
def asistencias_por_inscripcion(
    id_inscripcion: int,
    db: Session = Depends(get_db),
    _=Depends(require_rol("admin", "superadmin", "docente", "estudiante"))
):
    return db.query(Asistencia).filter(
        Asistencia.id_inscripcion == id_inscripcion
    ).all()

# ── POST registrar asistencia ─────────────────────────────
@router.post("/", response_model=AsistenciaResponse, status_code=status.HTTP_201_CREATED)
def registrar_asistencia(
    asistencia: AsistenciaCreate,
    db: Session = Depends(get_db),
    _=Depends(require_rol("admin", "superadmin", "docente"))
):
    estados_validos = ["presente", "ausente", "justificado"]
    if asistencia.estado not in estados_validos:
        raise HTTPException(status_code=400, detail=f"Estado inválido. Use: {estados_validos}")

    # Verificar inscripcion existe
    inscripcion = db.query(Inscripcion).filter(
        Inscripcion.id_inscripcion == asistencia.id_inscripcion
    ).first()
    if not inscripcion:
        raise HTTPException(status_code=404, detail="Inscripcion no encontrada")

    # Verificar asistencia duplicada en la misma fecha
    existe = db.query(Asistencia).filter(
        Asistencia.id_inscripcion == asistencia.id_inscripcion,
        Asistencia.fecha_asistencia == asistencia.fecha_asistencia
    ).first()
    if existe:
        raise HTTPException(status_code=400, detail="Ya existe asistencia registrada para esta fecha")

    nueva = Asistencia(**asistencia.model_dump())
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva

# ── PUT actualizar asistencia ─────────────────────────────
@router.put("/{id_asistencia}", response_model=AsistenciaResponse)
def actualizar_asistencia(
    id_asistencia: int,
    datos: AsistenciaUpdate,
    db: Session = Depends(get_db),
    _=Depends(require_rol("admin", "superadmin", "docente"))
):
    asistencia = db.query(Asistencia).filter(
        Asistencia.id_asistencia == id_asistencia
    ).first()
    if not asistencia:
        raise HTTPException(status_code=404, detail="Asistencia no encontrada")

    for campo, valor in datos.model_dump(exclude_unset=True).items():
        setattr(asistencia, campo, valor)

    db.commit()
    db.refresh(asistencia)
    return asistencia

# ── DELETE eliminar asistencia ────────────────────────────
@router.delete("/{id_asistencia}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_asistencia(
    id_asistencia: int,
    db: Session = Depends(get_db),
    _=Depends(require_rol("admin", "superadmin", "docente"))
):
    asistencia = db.query(Asistencia).filter(
        Asistencia.id_asistencia == id_asistencia
    ).first()
    if not asistencia:
        raise HTTPException(status_code=404, detail="Asistencia no encontrada")
    db.delete(asistencia)
    db.commit()