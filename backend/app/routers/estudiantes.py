from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.estudiante import Estudiante
from app.models.usuario import Usuario
from app.schemas.estudiante import EstudianteCreate, EstudianteResponse, EstudianteUpdate
from app.core.dependencies import require_rol
from datetime import datetime

router = APIRouter(prefix="/estudiantes", tags=["Estudiantes"])

@router.get("/", response_model=List[EstudianteResponse])
def listar_estudiantes(
    db: Session = Depends(get_db),
    _=Depends(require_rol("admin", "superadmin", "docente"))
):
    return db.query(Estudiante).all()

@router.get("/{id_estudiante}", response_model=EstudianteResponse)
def obtener_estudiante(
    id_estudiante: int,
    db: Session = Depends(get_db),
    _=Depends(require_rol("admin", "superadmin", "docente", "estudiante"))
):
    estudiante = db.query(Estudiante).filter(Estudiante.id_estudiante == id_estudiante).first()
    if not estudiante:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    return estudiante

@router.post("/", response_model=EstudianteResponse, status_code=status.HTTP_201_CREATED)
def crear_estudiante(
    estudiante: EstudianteCreate,
    db: Session = Depends(get_db),
    _=Depends(require_rol("admin", "superadmin"))
):
    usuario = db.query(Usuario).filter(Usuario.id_usuario == estudiante.id_usuario).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    existe = db.query(Estudiante).filter(Estudiante.id_usuario == estudiante.id_usuario).first()
    if existe:
        raise HTTPException(status_code=400, detail="Este usuario ya tiene perfil de estudiante")

    nuevo = Estudiante(**estudiante.model_dump())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

@router.put("/{id_estudiante}", response_model=EstudianteResponse)
def actualizar_estudiante(
    id_estudiante: int,
    datos: EstudianteUpdate,
    db: Session = Depends(get_db),
    _=Depends(require_rol("admin", "superadmin", "estudiante"))
):
    estudiante = db.query(Estudiante).filter(Estudiante.id_estudiante == id_estudiante).first()
    if not estudiante:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")

    for campo, valor in datos.model_dump(exclude_unset=True).items():
        setattr(estudiante, campo, valor)

    estudiante.updated_at = datetime.now()
    db.commit()
    db.refresh(estudiante)
    return estudiante

@router.delete("/{id_estudiante}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_estudiante(
    id_estudiante: int,
    db: Session = Depends(get_db),
    _=Depends(require_rol("superadmin"))
):
    estudiante = db.query(Estudiante).filter(Estudiante.id_estudiante == id_estudiante).first()
    if not estudiante:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    db.delete(estudiante)
    db.commit()