from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.encuesta import EncuestaSatisfaccion
from app.models.inscripcion import Inscripcion
from app.schemas.encuesta import EncuestaCreate, EncuestaResponse
from app.core.dependencies import require_rol

router = APIRouter(prefix="/encuestas", tags=["Encuestas"])

# ── GET todas las encuestas ───────────────────────────────
@router.get("/", response_model=List[EncuestaResponse])
def listar_encuestas(
    db: Session = Depends(get_db),
    _=Depends(require_rol("admin", "superadmin"))
):
    return db.query(EncuestaSatisfaccion).all()

# ── GET encuesta por inscripcion ──────────────────────────
@router.get("/inscripcion/{id_inscripcion}", response_model=EncuestaResponse)
def encuesta_por_inscripcion(
    id_inscripcion: int,
    db: Session = Depends(get_db),
    _=Depends(require_rol("admin", "superadmin", "estudiante"))
):
    encuesta = db.query(EncuestaSatisfaccion).filter(
        EncuestaSatisfaccion.id_inscripcion == id_inscripcion
    ).first()
    if not encuesta:
        raise HTTPException(status_code=404, detail="Encuesta no encontrada")
    return encuesta

# ── POST crear encuesta ───────────────────────────────────
@router.post("/", response_model=EncuestaResponse, status_code=status.HTTP_201_CREATED)
def crear_encuesta(
    encuesta: EncuestaCreate,
    db: Session = Depends(get_db),
    _=Depends(require_rol("estudiante"))
):
    # Verificar inscripcion existe
    inscripcion = db.query(Inscripcion).filter(
        Inscripcion.id_inscripcion == encuesta.id_inscripcion
    ).first()
    if not inscripcion:
        raise HTTPException(status_code=404, detail="Inscripcion no encontrada")

    # Verificar que no haya llenado ya la encuesta
    existe = db.query(EncuestaSatisfaccion).filter(
        EncuestaSatisfaccion.id_inscripcion == encuesta.id_inscripcion
    ).first()
    if existe:
        raise HTTPException(status_code=400, detail="Ya llenaste la encuesta para esta inscripcion")

    # Validar calificaciones entre 1 y 5
    if not (1 <= encuesta.calificacion_curso <= 5):
        raise HTTPException(status_code=400, detail="La calificacion del curso debe ser entre 1 y 5")
    if not (1 <= encuesta.calificacion_docente <= 5):
        raise HTTPException(status_code=400, detail="La calificacion del docente debe ser entre 1 y 5")

    nueva = EncuestaSatisfaccion(**encuesta.model_dump())
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva

# ── GET promedio por curso ────────────────────────────────
@router.get("/promedios/curso/{id_curso}")
def promedios_por_curso(
    id_curso: int,
    db: Session = Depends(get_db),
    _=Depends(require_rol("admin", "superadmin", "docente"))
):
    from app.models.inscripcion import Inscripcion
    from app.models.curso import Horario
    from sqlalchemy import func

    promedio = db.query(
        func.avg(EncuestaSatisfaccion.calificacion_curso).label("promedio_curso"),
        func.avg(EncuestaSatisfaccion.calificacion_docente).label("promedio_docente"),
        func.count(EncuestaSatisfaccion.id_encuesta).label("total_encuestas")
    ).join(
        Inscripcion, EncuestaSatisfaccion.id_inscripcion == Inscripcion.id_inscripcion
    ).join(
        Horario, Inscripcion.id_horario == Horario.id_horario
    ).filter(
        Horario.id_curso == id_curso
    ).first()

    return {
        "id_curso": id_curso,
        "promedio_curso": round(float(promedio.promedio_curso), 2) if promedio.promedio_curso else 0,
        "promedio_docente": round(float(promedio.promedio_docente), 2) if promedio.promedio_docente else 0,
        "total_encuestas": promedio.total_encuestas
    }