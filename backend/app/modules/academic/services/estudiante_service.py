from sqlalchemy.orm import Session
from typing import Optional, List, Dict, Any
from fastapi import HTTPException, status

from app.modules.auth.models.usuario import Usuario  # ← Importar SOLO en servicios
from app.modules.academic.models.estudiante import Estudiante
from app.modules.academic.schemas.estudiante import EstudianteCreate, EstudianteUpdate

def crear_estudiante(db: Session, data: EstudianteCreate) -> Estudiante:
    # Verificar que el usuario exista
    user = db.get(Usuario, data.id_usuario)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario base no encontrado")
    
    # Verificar que no tenga ya perfil de estudiante
    existing = db.get(Estudiante, data.id_usuario)
    if existing:
        raise HTTPException(status_code=400, detail="El usuario ya tiene perfil de estudiante")
    
    nuevo = Estudiante(
        id_estudiante=data.id_usuario,
        institucion=data.institucion,
        fecha_ingreso=data.fecha_ingreso
    )
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

def obtener_estudiante(db: Session, id_usuario: int) -> Optional[Dict[str, Any]]:
    """Obtiene estudiante + datos del usuario en una sola función"""
    est = db.get(Estudiante, id_usuario)
    if not est:
        return None
    
    # 🔹 Consulta manual del usuario (reemplaza relationship)
    user = db.get(Usuario, id_usuario)
    
    return {
        "id_estudiante": est.id_estudiante,
        "institucion": est.institucion,
        "fecha_ingreso": est.fecha_ingreso,
        "created_at": est.created_at,
        "updated_at": est.updated_at,
        # Datos del usuario obtenidos manualmente
        "ci": user.ci if user else None,
        "nombre": user.nombre if user else None,
        "ape_paterno": user.ape_paterno if user else None,
        "ape_materno": user.ape_materno if user else None,
        "correo_electronico": user.correo_electronico if user else None,
        "estado": user.estado if user else None,
    }

def listar_estudiantes(db: Session, skip: int = 0, limit: int = 20) -> List[Dict[str, Any]]:
    """Lista estudiantes con datos de usuario usando JOIN manual"""
    from sqlalchemy import select
    
    stmt = select(Estudiante, Usuario).join(
        Usuario, Estudiante.id_estudiante == Usuario.id_usuario
    ).offset(skip).limit(limit)
    
    results = db.execute(stmt).all()
    
    return [
        {
            "id_estudiante": est.id_estudiante,
            "institucion": est.institucion,
            "fecha_ingreso": est.fecha_ingreso,
            "ci": user.ci,
            "nombre": user.nombre,
            "ape_paterno": user.ape_paterno,
            "ape_materno": user.ape_materno,
            "correo_electronico": user.correo_electronico,
            "estado": user.estado,
        } for est, user in results
    ]

def actualizar_estudiante(db: Session, id_usuario: int, data: EstudianteUpdate) -> Optional[Dict[str, Any]]:
    est = db.get(Estudiante, id_usuario)
    if not est:
        return None
    
    for key, value in data.model_dump(exclude_unset=True).items():
        if hasattr(est, key):
            setattr(est, key, value)
    
    db.commit()
    db.refresh(est)
    return obtener_estudiante(db, id_usuario)

def eliminar_estudiante(db: Session, id_usuario: int) -> bool:
    est = db.get(Estudiante, id_usuario)
    if not est:
        return False
    db.delete(est)
    db.commit()
    return True