from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.models.curso import Horario, Curso, Aula
from app.models.docente import Docente
from app.core.dependencies import require_rol
from pydantic import BaseModel
from datetime import datetime, time

router = APIRouter(prefix="/horarios", tags=["Horarios"])

# ── Schemas inline ────────────────────────────────────────
class HorarioCreate(BaseModel):
    id_curso: int
    id_aula: Optional[int] = None
    id_docente: Optional[int] = None
    grupo: Optional[str] = None
    dia_semana: Optional[str] = None
    hora_inicio: Optional[time] = None
    hora_fin: Optional[time] = None
    cantidad_dias: Optional[int] = None
    modalidad: Optional[str] = None

class HorarioUpdate(BaseModel):
    id_aula: Optional[int] = None
    id_docente: Optional[int] = None
    grupo: Optional[str] = None
    dia_semana: Optional[str] = None
    hora_inicio: Optional[time] = None
    hora_fin: Optional[time] = None
    cantidad_dias: Optional[int] = None
    modalidad: Optional[str] = None
    estado: Optional[str] = None

class HorarioResponse(BaseModel):
    id_horario: int
    id_curso: int
    id_aula: Optional[int] = None
    id_docente: Optional[int] = None
    grupo: Optional[str] = None
    dia_semana: Optional[str] = None
    hora_inicio: Optional[time] = None
    hora_fin: Optional[time] = None
    cantidad_dias: Optional[int] = None
    modalidad: Optional[str] = None
    estado: Optional[str] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# ── GET todos los horarios ────────────────────────────────
@router.get("/", response_model=List[HorarioResponse])
def listar_horarios(db: Session = Depends(get_db)):
    return db.query(Horario).all()

# ── GET horarios por curso ────────────────────────────────
@router.get("/curso/{id_curso}", response_model=List[HorarioResponse])
def horarios_por_curso(id_curso: int, db: Session = Depends(get_db)):
    return db.query(Horario).filter(Horario.id_curso == id_curso).all()

# ── GET horario por ID ────────────────────────────────────
@router.get("/{id_horario}", response_model=HorarioResponse)
def obtener_horario(id_horario: int, db: Session = Depends(get_db)):
    horario = db.query(Horario).filter(Horario.id_horario == id_horario).first()
    if not horario:
        raise HTTPException(status_code=404, detail="Horario no encontrado")
    return horario

# ── POST crear horario ────────────────────────────────────
@router.post("/", response_model=HorarioResponse, status_code=status.HTTP_201_CREATED)
def crear_horario(
    horario: HorarioCreate,
    db: Session = Depends(get_db),
    _=Depends(require_rol("admin", "superadmin"))
):
    curso = db.query(Curso).filter(Curso.id_curso == horario.id_curso).first()
    if not curso:
        raise HTTPException(status_code=404, detail="Curso no encontrado")

    nuevo = Horario(**horario.model_dump(), estado="activo")
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

# ── PUT actualizar horario ────────────────────────────────
@router.put("/{id_horario}", response_model=HorarioResponse)
def actualizar_horario(
    id_horario: int,
    datos: HorarioUpdate,
    db: Session = Depends(get_db),
    _=Depends(require_rol("admin", "superadmin"))
):
    horario = db.query(Horario).filter(Horario.id_horario == id_horario).first()
    if not horario:
        raise HTTPException(status_code=404, detail="Horario no encontrado")

    for campo, valor in datos.model_dump(exclude_unset=True).items():
        setattr(horario, campo, valor)

    horario.updated_at = datetime.now()
    db.commit()
    db.refresh(horario)
    return horario

# ── DELETE eliminar horario ───────────────────────────────
@router.delete("/{id_horario}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_horario(
    id_horario: int,
    db: Session = Depends(get_db),
    _=Depends(require_rol("admin", "superadmin"))
):
    horario = db.query(Horario).filter(Horario.id_horario == id_horario).first()
    if not horario:
        raise HTTPException(status_code=404, detail="Horario no encontrado")
    db.delete(horario)
    db.commit()

# ── PATCH cambiar estado ──────────────────────────────────
@router.patch("/{id_horario}/estado", response_model=HorarioResponse)
def cambiar_estado(
    id_horario: int,
    estado: str,
    db: Session = Depends(get_db),
    _=Depends(require_rol("admin", "superadmin"))
):
    estados_validos = ["activo", "inactivo"]
    if estado not in estados_validos:
        raise HTTPException(status_code=400, detail=f"Estado inválido. Use: {estados_validos}")

    horario = db.query(Horario).filter(Horario.id_horario == id_horario).first()
    if not horario:
        raise HTTPException(status_code=404, detail="Horario no encontrado")

    horario.estado = estado
    horario.updated_at = datetime.now()
    db.commit()
    db.refresh(horario)
    return horario