from sqlalchemy.orm import Session
from typing import Optional, List, Dict, Any
from fastapi import HTTPException, status

from app.modules.auth.models.usuario import Usuario
from app.modules.academic.models.docente import Docente
from app.modules.academic.schemas.docente import DocenteCreate, DocenteUpdate

def crear_docente(db: Session, data: DocenteCreate) -> Docente:
    user = db.get(Usuario, data.id_usuario)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario base no encontrado")
    
    existing = db.get(Docente, data.id_usuario)
    if existing:
        raise HTTPException(status_code=400, detail="El usuario ya tiene perfil de docente")
    
    nuevo = Docente(
        id_docente=data.id_usuario,
        especialidad=data.especialidad,
        grado_academico=data.grado_academico,
        anios_experiencia=data.anios_experiencia,
        fecha_inicio=data.fecha_inicio,
        estado=data.estado or "activo"
    )
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

def obtener_docente(db: Session, id_usuario: int) -> Optional[Dict[str, Any]]:
    doc = db.get(Docente, id_usuario)
    if not doc:
        return None
    
    user = db.get(Usuario, id_usuario)
    
    return {
        "id_docente": doc.id_docente,
        "especialidad": doc.especialidad,
        "grado_academico": doc.grado_academico,
        "anios_experiencia": doc.anios_experiencia,
        "fecha_inicio": doc.fecha_inicio,
        "estado": doc.estado,
        "created_at": doc.created_at,
        "updated_at": doc.updated_at,
        "ci": user.ci if user else None,
        "nombre": user.nombre if user else None,
        "ape_paterno": user.ape_paterno if user else None,
        "ape_materno": user.ape_materno if user else None,
        "correo_electronico": user.correo_electronico if user else None,
    }

def listar_docentes(db: Session, skip: int = 0, limit: int = 20) -> List[Dict[str, Any]]:
    from sqlalchemy import select
    
    stmt = select(Docente, Usuario).join(
        Usuario, Docente.id_docente == Usuario.id_usuario
    ).offset(skip).limit(limit)
    
    results = db.execute(stmt).all()
    
    docentes = []
    for doc, user in results:
        docentes.append({
            "id_docente": doc.id_docente,
            "especialidad": doc.especialidad,
            "grado_academico": doc.grado_academico,
            "anios_experiencia": doc.anios_experiencia,
            "fecha_inicio": doc.fecha_inicio,
            "estado": doc.estado,
            "created_at": doc.created_at,
            "updated_at": doc.updated_at,
            "ci": user.ci if user else None,
            "nombre": user.nombre if user else None,
            "ape_paterno": user.ape_paterno if user else None,
            "ape_materno": user.ape_materno if user else None,
            "correo_electronico": user.correo_electronico if user else None,
        })
    
    return docentes 

def actualizar_docente(db: Session, id_usuario: int, data: DocenteUpdate) -> Optional[Dict[str, Any]]:
    docente = db.get(Docente, id_usuario)
    if not docente:
        return None
    
    for field, value in data.dict(exclude_unset=True).items():
        setattr(docente, field, value)
    
    db.commit()
    db.refresh(docente)
    
    user = db.get(Usuario, id_usuario)
    
    return {
        "id_docente": docente.id_docente,
        "especialidad": docente.especialidad,
        "grado_academico": docente.grado_academico,
        "anios_experiencia": docente.anios_experiencia,
        "fecha_inicio": docente.fecha_inicio,
        "estado": docente.estado,
        "created_at": docente.created_at,
        "updated_at": docente.updated_at,
        "ci": user.ci if user else None,
        "nombre": user.nombre if user else None,
        "ape_paterno": user.ape_paterno if user else None,
        "ape_materno": user.ape_materno if user else None,
        "correo_electronico": user.correo_electronico if user else None,
    }

def eliminar_docente(db: Session, id_usuario: int) -> bool:
    docente = db.get(Docente, id_usuario)
    if not docente:
        return False
    db.delete(docente)
    db.commit()
    return True
    
# ... listar_docente, actualizar_docente, eliminar_docente siguen el mismo patrón ...