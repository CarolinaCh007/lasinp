from sqlalchemy.orm import Session
from sqlalchemy import select, exc
from typing import Optional, List
from fastapi import HTTPException
from datetime import datetime
import hashlib, uuid
from decimal import Decimal

from app.modules.enrollment.models.inscripcion import Inscripcion
from app.modules.evaluation.models import *
from app.modules.evaluation.schemas import *

# 🔹 HELPERS CRUD (genéricos para cada tabla)
def _crear(db: Session, modelo, data):
    try:
        obj = modelo(**data.model_dump())
        db.add(obj); db.commit(); db.refresh(obj); return obj
    except exc.IntegrityError:
        db.rollback()
        raise HTTPException(400, "Error de integridad: verifica FKs o constraints únicos.")

def _obtener(db: Session, modelo, id: int):
    """Helper genérico: retorna el objeto o None si no existe"""
    return db.get(modelo, id)

def _actualizar(db: Session, id: int, modelo, data):
    obj = db.get(modelo, id)
    if not obj: raise HTTPException(404, f"{modelo.__tablename__} no encontrado")
    for k, v in data.model_dump(exclude_unset=True).items(): setattr(obj, k, v)
    try: db.commit(); db.refresh(obj); return obj
    except exc.IntegrityError:
        db.rollback()
        raise HTTPException(400, "Error de integridad al actualizar.")
def _eliminar(db: Session, modelo, id: int):
    obj = db.get(modelo, id)
    if not obj: raise HTTPException(404, f"{modelo.__tablename__} no encontrado")
    try: db.delete(obj); db.commit(); return True
    except exc.IntegrityError:
        db.rollback()
        raise HTTPException(400, "No se puede eliminar: tiene registros dependientes.")

# 🔹 CRUD ESPECÍFICOS (envoltorios)
def crear_tipo(db, d): return _crear(db, TipoEvaluacion, d)
def crear_actividad(db, d): return _crear(db, ActividadFinal, d)
def crear_respuesta(db, d): return _crear(db, RespActividad, d)
def crear_calificacion(db, d): return _crear(db, Calificacion, d)
def crear_asistencia(db, d): return _crear(db, Asistencia, d)
def crear_encuesta(db, d): return _crear(db, EncuestaSatisfaccion, d)

# 🔹 LÓGICA DE NEGOCIO CLAVE
def calcular_nota_final(db: Session, id_inscripcion: int) -> Decimal:
    """Calcula nota ponderada final y actualiza inscripcion.nota_final"""
    stmt = select(Calificacion.puntaje, TipoEvaluacion.peso_porcentual).join(
        TipoEvaluacion, Calificacion.id_tipo == TipoEvaluacion.id_tipo
    ).where(Calificacion.id_inscripcion == id_inscripcion)
    rows = db.execute(stmt).all()
    
    if not rows:
        raise HTTPException(404, "No hay calificaciones registradas para esta inscripción.")
        
    total_pesos = sum(float(r.peso_porcentual or 0) for r in rows)
    if total_pesos == 0: total_pesos = 100  # Fallback si no hay pesos
    
    nota_final = sum((float(r.puntaje or 0) * (float(r.peso_porcentual or 0) / total_pesos)) for r in rows)
    
    insc = db.get(Inscripcion, id_inscripcion)
    if not insc: raise HTTPException(404, "Inscripción no encontrada")
    
    insc.nota_final = Decimal(str(round(nota_final, 2)))
    db.commit()
    db.refresh(insc)
    return insc.nota_final

def generar_certificado(db: Session, id_inscripcion: int) -> Certificado:
    """Genera certificado solo si nota_final >= 51 y estado activo"""
    insc = db.get(Inscripcion, id_inscripcion)
    if not insc: raise HTTPException(404, "Inscripción no encontrada")
    
    if insc.nota_final is None or float(insc.nota_final) < 51:
        raise HTTPException(400, "No se puede generar: nota final < 51 o no calculada.")
    if insc.estado != "activo":
        raise HTTPException(400, "No se puede generar: inscripción no está activa.")
        
    # Verificar si ya existe
    exist = db.query(Certificado).filter(Certificado.id_inscripcion == id_inscripcion).first()
    if exist: return exist
    
    # Generar datos únicos
    codigo = f"CERT-{id_inscripcion}-{uuid.uuid4().hex[:8].upper()}"
    hash_val = hashlib.sha256(f"{codigo}{insc.nota_final}{datetime.utcnow().isoformat()}".encode()).hexdigest()
    
    nuevo = Certificado(
        id_inscripcion=id_inscripcion,
        codigo_verificacion=codigo,
        estado="pendiente",
        hash_certificado=hash_val,
        qr_url=f"https://tu-dominio.edu/verify/{codigo}"
    )
    db.add(nuevo); db.commit(); db.refresh(nuevo)
    return nuevo

def listar_por_inscripcion(db, modelo, id_inscripcion: int):
    stmt = select(modelo).where(modelo.id_inscripcion == id_inscripcion)
    return db.execute(stmt).scalars().all()