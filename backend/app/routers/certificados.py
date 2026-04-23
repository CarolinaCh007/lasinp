from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.certificado import Certificado
from app.models.inscripcion import Inscripcion
from app.schemas.certificado import (
    CertificadoCreate, CertificadoResponse, CertificadoUpdate,
    VerificarCertificadoRequest, VerificarCertificadoResponse
)
from app.core.dependencies import require_rol
from datetime import date, datetime
import uuid

router = APIRouter(prefix="/certificados", tags=["Certificados"])

# ── GET todos los certificados ────────────────────────────
@router.get("/", response_model=List[CertificadoResponse])
def listar_certificados(
    db: Session = Depends(get_db),
    _=Depends(require_rol("admin", "superadmin"))
):
    return db.query(Certificado).all()

# ── GET certificado por inscripcion ───────────────────────
@router.get("/inscripcion/{id_inscripcion}", response_model=CertificadoResponse)
def certificado_por_inscripcion(
    id_inscripcion: int,
    db: Session = Depends(get_db),
    _=Depends(require_rol("admin", "superadmin", "estudiante"))
):
    certificado = db.query(Certificado).filter(
        Certificado.id_inscripcion == id_inscripcion
    ).first()
    if not certificado:
        raise HTTPException(status_code=404, detail="Certificado no encontrado")
    return certificado

# ── POST verificar certificado (publico) ──────────────────
@router.post("/verificar", response_model=VerificarCertificadoResponse)
def verificar_certificado(
    datos: VerificarCertificadoRequest,
    db: Session = Depends(get_db)
):
    certificado = db.query(Certificado).filter(
        Certificado.codigo_verificacion == datos.codigo_verificacion
    ).first()

    if not certificado:
        return {
            "valido": False,
            "mensaje": "Certificado no encontrado",
            "certificado": None
        }

    if certificado.estado == "anulado":
        return {
            "valido": False,
            "mensaje": "Este certificado ha sido anulado",
            "certificado": None
        }

    return {
        "valido": True,
        "mensaje": "Certificado válido",
        "certificado": certificado
    }

# ── POST emitir certificado ───────────────────────────────
@router.post("/", response_model=CertificadoResponse, status_code=status.HTTP_201_CREATED)
def emitir_certificado(
    datos: CertificadoCreate,
    db: Session = Depends(get_db),
    _=Depends(require_rol("admin", "superadmin"))
):
    # Verificar inscripcion existe
    inscripcion = db.query(Inscripcion).filter(
        Inscripcion.id_inscripcion == datos.id_inscripcion
    ).first()
    if not inscripcion:
        raise HTTPException(status_code=404, detail="Inscripcion no encontrada")

    # Verificar que no tenga ya un certificado
    existe = db.query(Certificado).filter(
        Certificado.id_inscripcion == datos.id_inscripcion
    ).first()
    if existe:
        raise HTTPException(status_code=400, detail="Ya existe un certificado para esta inscripcion")

    # Generar codigo unico
    codigo = str(uuid.uuid4()).replace("-", "").upper()[:12]

    nuevo = Certificado(
        id_inscripcion=datos.id_inscripcion,
        codigo_verificacion=codigo,
        fecha_emision=date.today(),
        estado="emitido"
    )
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

# ── PATCH anular certificado ──────────────────────────────
@router.patch("/{id_certificado}/anular", response_model=CertificadoResponse)
def anular_certificado(
    id_certificado: int,
    db: Session = Depends(get_db),
    _=Depends(require_rol("superadmin"))
):
    certificado = db.query(Certificado).filter(
        Certificado.id_certificado == id_certificado
    ).first()
    if not certificado:
        raise HTTPException(status_code=404, detail="Certificado no encontrado")

    certificado.estado = "anulado"
    certificado.updated_at = datetime.now()
    db.commit()
    db.refresh(certificado)
    return certificado