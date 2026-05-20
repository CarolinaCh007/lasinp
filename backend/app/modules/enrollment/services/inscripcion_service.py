from sqlalchemy.orm import Session
from sqlalchemy import select, exc
from typing import Optional, List, Dict, Any
from fastapi import HTTPException, status
from app.modules.enrollment.models.inscripcion import Inscripcion
from app.modules.enrollment.models.pago import Pago
from app.modules.enrollment.schemas.inscripcion import InscripcionCreate, InscripcionUpdate
from app.modules.enrollment.schemas.inscripcion import InscripcionConPagoRequest

def crear_inscripcion(db: Session, data: InscripcionCreate) -> Inscripcion:
    try:
        nuevo = Inscripcion(**data.model_dump())
        db.add(nuevo); db.commit(); db.refresh(nuevo); return nuevo
    except exc.IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Error de integridad: verifica que id_horario e id_estudiante existan.")

def obtener_inscripcion(db: Session, id_inscripcion: int) -> Optional[Inscripcion]:
    return db.get(Inscripcion, id_inscripcion)

def listar_inscripciones(db: Session, id_estudiante: Optional[int] = None, id_horario: Optional[int] = None, skip: int = 0, limit: int = 20) -> List[Inscripcion]:
    stmt = select(Inscripcion)
    if id_estudiante: stmt = stmt.where(Inscripcion.id_estudiante == id_estudiante)
    if id_horario: stmt = stmt.where(Inscripcion.id_horario == id_horario)
    return db.execute(stmt.offset(skip).limit(limit)).scalars().all()

def actualizar_inscripcion(db: Session, id_inscripcion: int, data: InscripcionUpdate) -> Optional[Inscripcion]:
    insc = db.get(Inscripcion, id_inscripcion)
    if not insc: return None
    for k, v in data.model_dump(exclude_unset=True).items(): setattr(insc, k, v)
    try: db.commit(); db.refresh(insc); return insc
    except exc.IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Error de integridad al actualizar.")

def eliminar_inscripcion(db: Session, id_inscripcion: int) -> bool:
    insc = db.get(Inscripcion, id_inscripcion)
    if not insc: return False
    try: db.delete(insc); db.commit(); return True
    except exc.IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="No se puede eliminar: tiene registros dependientes (pagos, calificaciones, etc.).")

def crear_inscripcion_con_pago(db: Session, data: InscripcionConPagoRequest) -> Dict[str, Any]:
    """Crea inscripción + primer pago en transacción atómica"""
    try:
        # 1. Crear Inscripción (estado inicial: pendiente)
        insc_data = data.inscripcion.model_dump()
        insc_data["estado"] = insc_data.get("estado") or "pendiente"
        nueva_insc = Inscripcion(**insc_data)
        db.add(nueva_insc)
        db.flush()  # Obtiene id_inscripcion sin hacer commit aún

        # 2. Crear Pago vinculado (comprobante subido)
        pago_data = data.pago.model_dump()
        pago_data["id_inscripcion"] = nueva_insc.id_inscripcion
        nuevo_pago = Pago(**pago_data)
        db.add(nuevo_pago)

        db.commit()
        db.refresh(nueva_insc)
        db.refresh(nuevo_pago)
        return {"inscripcion": nueva_insc, "pago": nuevo_pago}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error al procesar inscripción y pago: {str(e)}")

def listar_inscritos_por_curso(db: Session, id_curso: int) -> List[Dict[str, Any]]:
    """Lista estudiantes inscritos a un curso específico (vía horario)"""
    from app.modules.scheduling.models.horario import Horario
    from app.modules.academic.models.estudiante import Estudiante
    from app.modules.auth.models.usuario import Usuario

    stmt = (
        select(Inscripcion, Usuario.nombre, Usuario.ape_paterno, Usuario.ape_materno, 
               Usuario.correo_electronico, Horario.id_curso)
        .join(Horario, Inscripcion.id_horario == Horario.id_horario)
        .join(Estudiante, Inscripcion.id_estudiante == Estudiante.id_estudiante)
        .join(Usuario, Estudiante.id_estudiante == Usuario.id_usuario)
        .where(Horario.id_curso == id_curso)
        .order_by(Inscripcion.fecha_inscripcion.desc())
    )
    results = db.execute(stmt).all()
    
    return [
        {
            "id_inscripcion": r.Inscripcion.id_inscripcion,
            "id_estudiante": r.Inscripcion.id_estudiante,
            "nombre_completo": f"{r.nombre} {r.ape_paterno} {r.ape_materno}",
            "correo": r.correo_electronico,
            "estado_inscripcion": r.Inscripcion.estado,
            "nota_final": r.Inscripcion.nota_final,
            "fecha_inscripcion": r.Inscripcion.fecha_inscripcion
        } for r in results
    ]

def actualizar_estado_inscripcion(db: Session, id_inscripcion: int, nuevo_estado: str) -> Optional[Inscripcion]:
    """Cambia estado de inscripción (ej: pendiente → activo tras validar comprobante)"""
    estados_validos = ["activo", "inactivo", "pendiente", "retirado"]
    if nuevo_estado not in estados_validos:
        raise HTTPException(status_code=400, detail=f"Estado inválido. Usa: {estados_validos}")
        
    insc = db.get(Inscripcion, id_inscripcion)
    if not insc: return None
    
    insc.estado = nuevo_estado
    db.commit()
    db.refresh(insc)
    return insc