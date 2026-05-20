from sqlalchemy.orm import Session
from sqlalchemy import select, exc
from fastapi import HTTPException, status
from typing import Optional, List, Dict, Any 
from app.modules.enrollment.models.pago import Pago
from app.modules.enrollment.schemas.pago import PagoCreate, PagoUpdate

def crear_pago(db: Session, data: PagoCreate) -> Pago:
    try:
        nuevo = Pago(**data.model_dump())
        db.add(nuevo); db.commit(); db.refresh(nuevo); return nuevo
    except exc.IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Error de integridad: verifica que id_inscripcion exista.")

def obtener_pago(db: Session, id_pago: int) -> Optional[Pago]:
    return db.get(Pago, id_pago)

def listar_pagos(db: Session, id_inscripcion: Optional[int] = None, skip: int = 0, limit: int = 20) -> List[Pago]:
    stmt = select(Pago)
    if id_inscripcion: stmt = stmt.where(Pago.id_inscripcion == id_inscripcion)
    return db.execute(stmt.order_by(Pago.fecha_pago.desc(), Pago.hora_pago.desc()).offset(skip).limit(limit)).scalars().all()

def actualizar_pago(db: Session, id_pago: int, data: PagoUpdate) -> Optional[Pago]:
    pago = db.get(Pago, id_pago)
    if not pago: return None
    for k, v in data.model_dump(exclude_unset=True).items(): setattr(pago, k, v)
    try: db.commit(); db.refresh(pago); return pago
    except exc.IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Error de integridad al actualizar.")

def eliminar_pago(db: Session, id_pago: int) -> bool:
    pago = db.get(Pago, id_pago)
    if not pago: return False
    db.delete(pago); db.commit(); return True

def listar_historial_pagos_estudiante(db: Session, id_estudiante: int) -> List[Dict[str, Any]]:
    """Historial completo de pagos de un estudiante (todos sus cursos/horarios)"""
    from app.modules.academic.models.estudiante import Estudiante
    from app.modules.scheduling.models.horario import Horario
    from app.modules.courses.models.curso import Curso

    stmt = (
        select(Pago, Inscripcion, Horario.id_curso, Curso.nombre)
        .join(Inscripcion, Pago.id_inscripcion == Inscripcion.id_inscripcion)
        .join(Horario, Inscripcion.id_horario == Horario.id_horario)
        .join(Curso, Horario.id_curso == Curso.id_curso)
        .join(Estudiante, Inscripcion.id_estudiante == Estudiante.id_estudiante)
        .where(Estudiante.id_estudiante == id_estudiante)
        .order_by(Pago.fecha_pago.desc(), Pago.hora_pago.desc())
    )
    results = db.execute(stmt).all()
    
    return [
        {
            "id_pago": r.Pago.id_pago,
            "id_inscripcion": r.Pago.id_inscripcion,
            "curso": r.nombre,
            "id_curso": r.Horario.id_curso,
            "precio": r.Pago.precio,
            "estado_pago": r.Pago.estado,
            "metodo_pago": r.Pago.metodo_pago,
            "fecha_pago": r.Pago.fecha_pago,
            "hora_pago": r.Pago.hora_pago,
            "comprobante_url": r.Pago.url_pasarela or r.Pago.codigo_recaudacion,
            "observaciones": r.Pago.observaciones
        } for r in results
    ]