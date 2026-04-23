from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.docente import Docente, Portafolio
from app.models.usuario import Usuario
from app.schemas.docente import (
    DocenteCreate, DocenteResponse, DocenteUpdate,
    PortafolioCreate, PortafolioResponse, PortafolioUpdate
)
from app.core.dependencies import require_rol
from datetime import datetime

router = APIRouter(prefix="/docentes", tags=["Docentes"])

@router.get("/", response_model=List[DocenteResponse])
def listar_docentes(db: Session = Depends(get_db)):
    return db.query(Docente).all()

@router.get("/{id_docente}", response_model=DocenteResponse)
def obtener_docente(id_docente: int, db: Session = Depends(get_db)):
    docente = db.query(Docente).filter(Docente.id_docente == id_docente).first()
    if not docente:
        raise HTTPException(status_code=404, detail="Docente no encontrado")
    return docente

@router.post("/", response_model=DocenteResponse, status_code=status.HTTP_201_CREATED)
def crear_docente(
    docente: DocenteCreate,
    db: Session = Depends(get_db),
    _=Depends(require_rol("admin", "superadmin"))
):
    usuario = db.query(Usuario).filter(Usuario.id_usuario == docente.id_usuario).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    existe = db.query(Docente).filter(Docente.id_usuario == docente.id_usuario).first()
    if existe:
        raise HTTPException(status_code=400, detail="Este usuario ya tiene perfil de docente")

    nuevo = Docente(**docente.model_dump(), estado="activo")
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

@router.put("/{id_docente}", response_model=DocenteResponse)
def actualizar_docente(
    id_docente: int,
    datos: DocenteUpdate,
    db: Session = Depends(get_db),
    _=Depends(require_rol("admin", "superadmin"))
):
    docente = db.query(Docente).filter(Docente.id_docente == id_docente).first()
    if not docente:
        raise HTTPException(status_code=404, detail="Docente no encontrado")

    for campo, valor in datos.model_dump(exclude_unset=True).items():
        setattr(docente, campo, valor)

    docente.updated_at = datetime.now()
    db.commit()
    db.refresh(docente)
    return docente

@router.delete("/{id_docente}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_docente(
    id_docente: int,
    db: Session = Depends(get_db),
    _=Depends(require_rol("superadmin"))
):
    docente = db.query(Docente).filter(Docente.id_docente == id_docente).first()
    if not docente:
        raise HTTPException(status_code=404, detail="Docente no encontrado")
    db.delete(docente)
    db.commit()

# ── Portafolio ────────────────────────────────────────────
@router.get("/{id_docente}/portafolio", response_model=PortafolioResponse)
def obtener_portafolio(id_docente: int, db: Session = Depends(get_db)):
    portafolio = db.query(Portafolio).filter(Portafolio.id_docente == id_docente).first()
    if not portafolio:
        raise HTTPException(status_code=404, detail="Portafolio no encontrado")
    return portafolio

@router.post("/{id_docente}/portafolio", response_model=PortafolioResponse, status_code=status.HTTP_201_CREATED)
def crear_portafolio(
    id_docente: int,
    portafolio: PortafolioCreate,
    db: Session = Depends(get_db),
    _=Depends(require_rol("admin", "superadmin", "docente"))
):
    existe = db.query(Portafolio).filter(Portafolio.id_docente == id_docente).first()
    if existe:
        raise HTTPException(status_code=400, detail="Este docente ya tiene portafolio")

    nuevo = Portafolio(**portafolio.model_dump())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

@router.put("/{id_docente}/portafolio", response_model=PortafolioResponse)
def actualizar_portafolio(
    id_docente: int,
    datos: PortafolioUpdate,
    db: Session = Depends(get_db),
    _=Depends(require_rol("admin", "superadmin", "docente"))
):
    portafolio = db.query(Portafolio).filter(Portafolio.id_docente == id_docente).first()
    if not portafolio:
        raise HTTPException(status_code=404, detail="Portafolio no encontrado")

    for campo, valor in datos.model_dump(exclude_unset=True).items():
        setattr(portafolio, campo, valor)

    db.commit()
    db.refresh(portafolio)
    return portafolio