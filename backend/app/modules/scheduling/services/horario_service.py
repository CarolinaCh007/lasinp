from sqlalchemy.orm import Session
from sqlalchemy import select, and_, or_
from typing import Optional, List
from datetime import time  # ← ¡IMPORTANTE: Agregar este import!
from fastapi import HTTPException, status

from app.modules.scheduling.models.horario import Horario
from app.modules.scheduling.schemas.horario import HorarioCreate, HorarioUpdate

def _hay_solapamiento(db: Session, nuevo: HorarioCreate, excluir_id: Optional[int] = None) -> bool:
    """
    Verifica si un nuevo horario se solapa con existentes.
    
    Reglas de solapamiento:
    1. Mismo día_semana + mismo id_aula + horas se cruzan
    2. Mismo día_semana + mismo id_docente + horas se cruzan
    
    Retorna True si HAY conflicto, False si está libre.
    """
    if not nuevo.dia_semana or not nuevo.hora_inicio or not nuevo.hora_fin:
        return False  # Sin día/hora no se puede validar solapamiento
    
    # Query base: mismos días y estado activo
    query = select(Horario).where(
        Horario.dia_semana == nuevo.dia_semana,
        Horario.estado == "activo"
    )
    
    if excluir_id:
        query = query.where(Horario.id_horario != excluir_id)
    
    horarios_existentes = db.execute(query).scalars().all()
    
    for h in horarios_existentes:
        if not h.hora_inicio or not h.hora_fin:
            continue
        
        # 🔹 Regla 1: Conflicto de AULA
        if nuevo.id_aula and h.id_aula == nuevo.id_aula:
            if _rangos_se_solapan(nuevo.hora_inicio, nuevo.hora_fin, h.hora_inicio, h.hora_fin):
                return True
        
        # 🔹 Regla 2: Conflicto de DOCENTE
        if nuevo.id_docente and h.id_docente == nuevo.id_docente:
            if _rangos_se_solapan(nuevo.hora_inicio, nuevo.hora_fin, h.hora_inicio, h.hora_fin):
                return True
    
    return False

def _rangos_se_solapan(inicio1: time, fin1: time, inicio2: time, fin2: time) -> bool:
    """Determina si dos rangos de tiempo se superponen"""
    # Convertir a minutos para comparar fácilmente
    def a_minutos(t: time) -> int:
        return t.hour * 60 + t.minute
    
    inicio1_min = a_minutos(inicio1)
    fin1_min = a_minutos(fin1)
    inicio2_min = a_minutos(inicio2)
    fin2_min = a_minutos(fin2)
    
    # Dos rangos se solapan si uno comienza antes de que el otro termine
    return inicio1_min < fin2_min and inicio2_min < fin1_min

def crear_horario(db: Session, data: HorarioCreate) -> Horario:
    # 🔹 Validación CRÍTICA: verificar solapamientos
    if _hay_solapamiento(db, data):
        raise HTTPException(
            status_code=400,
            detail="Conflicto de horario: el aula o docente ya está ocupado en ese día y hora."
        )
    
    nuevo = Horario(**data.model_dump())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

def obtener_horario(db: Session, id_horario: int) -> Optional[Horario]:
    return db.get(Horario, id_horario)

def listar_horarios(
    db: Session, 
    id_curso: Optional[int] = None,
    id_aula: Optional[int] = None,
    id_docente: Optional[int] = None,
    dia_semana: Optional[str] = None,
    skip: int = 0, 
    limit: int = 20
) -> List[Horario]:
    stmt = select(Horario)
    
    if id_curso:
        stmt = stmt.where(Horario.id_curso == id_curso)
    if id_aula:
        stmt = stmt.where(Horario.id_aula == id_aula)
    if id_docente:
        stmt = stmt.where(Horario.id_docente == id_docente)
    if dia_semana:
        stmt = stmt.where(Horario.dia_semana == dia_semana)
    
    return db.execute(stmt.offset(skip).limit(limit)).scalars().all()

def actualizar_horario(db: Session, id_horario: int, data: HorarioUpdate) -> Optional[Horario]:
    horario = db.get(Horario, id_horario)
    if not horario:
        return None
    
    # Si cambian día/hora/aula/docente, re-validar solapamientos
    campos_criticos = ["dia_semana", "hora_inicio", "hora_fin", "id_aula", "id_docente"]
    if any(getattr(data, campo, None) is not None for campo in campos_criticos):
        # Crear objeto temporal con los nuevos valores para validar
        temp_data = HorarioCreate(
            id_curso=getattr(data, "id_curso", horario.id_curso),
            id_aula=getattr(data, "id_aula", horario.id_aula),
            id_docente=getattr(data, "id_docente", horario.id_docente),
            dia_semana=getattr(data, "dia_semana", horario.dia_semana),
            hora_inicio=getattr(data, "hora_inicio", horario.hora_inicio),
            hora_fin=getattr(data, "hora_fin", horario.hora_fin),
        )
        if _hay_solapamiento(db, temp_data, excluir_id=id_horario):
            raise HTTPException(
                status_code=400,
                detail="Conflicto de horario: el aula o docente ya está ocupado en ese día y hora."
            )
    
    for key, value in data.model_dump(exclude_unset=True).items():
        if hasattr(horario, key):
            setattr(horario, key, value)
    
    db.commit()
    db.refresh(horario)
    return horario

def eliminar_horario(db: Session, id_horario: int) -> bool:
    horario = db.get(Horario, id_horario)
    if not horario:
        return False
    db.delete(horario)
    db.commit()
    return True