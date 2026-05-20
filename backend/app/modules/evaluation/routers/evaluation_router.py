from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.core.security import get_current_user, require_role
from app.modules.auth.models.usuario import Usuario
from app.modules.evaluation.schemas import *
from app.modules.evaluation.services.evaluation_service import *

router = APIRouter(prefix="/evaluation", tags=["📊 Evaluación y Certificados"])

# =============================================================================
# 🔹 TIPOS DE EVALUACIÓN
# =============================================================================

@router.post("/tipos", response_model=TipoEvaluacionRead, status_code=status.HTTP_201_CREATED, operation_id="crear_tipo_evaluacion")
def crear_tipo_evaluacion(
    data: TipoEvaluacionCreate, 
    db: Session = Depends(get_db), 
    current_user: Usuario = Depends(require_role("ADMIN", "COORDINADOR"))
):
    return crear_tipo(db, data)

@router.get("/tipos/{id_tipo}", response_model=TipoEvaluacionRead, operation_id="obtener_tipo_evaluacion")
def obtener_tipo_evaluacion(
    id_tipo: int, 
    db: Session = Depends(get_db), 
    current_user: Usuario = Depends(get_current_user)
):
    result = _obtener(db, TipoEvaluacion, id_tipo)
    if not result:
        raise HTTPException(status_code=404, detail="Tipo de evaluación no encontrado")
    return result

# =============================================================================
# 🔹 ACTIVIDADES FINALES
# =============================================================================

@router.post("/actividades", response_model=ActividadFinalRead, status_code=status.HTTP_201_CREATED, operation_id="crear_actividad")
def crear_actividad_endpoint(
    data: ActividadFinalCreate, 
    db: Session = Depends(get_db), 
    current_user: Usuario = Depends(require_role("DOCENTE", "ADMIN"))
):
    return crear_actividad(db, data)

@router.put("/actividades/{id_actividad}", response_model=ActividadFinalRead, operation_id="actualizar_actividad")
def actualizar_actividad_endpoint(
    id_actividad: int, 
    data: ActividadFinalUpdate, 
    db: Session = Depends(get_db), 
    current_user: Usuario = Depends(require_role("DOCENTE", "ADMIN"))
):
    return _actualizar(db, id_actividad, ActividadFinal, data)

# =============================================================================
# 🔹 RESPUESTAS / ENTREGAS DE ESTUDIANTES
# =============================================================================

@router.post("/respuestas", response_model=RespActividadRead, status_code=status.HTTP_201_CREATED, operation_id="crear_respuesta")
def crear_respuesta_endpoint(
    data: RespActividadCreate, 
    db: Session = Depends(get_db), 
    current_user: Usuario = Depends(get_current_user)
):
    # Validar que el estudiante solo entregue para sus propias inscripciones
    from app.modules.enrollment.models.inscripcion import Inscripcion
    insc = db.get(Inscripcion, data.id_inscripcion)
    if not insc:
        raise HTTPException(status_code=404, detail="Inscripción no encontrada")
    # Aquí podrías agregar: if current_user.id_usuario != insc.id_estudiante: ...
    return crear_respuesta(db, data)

@router.get("/respuestas/inscripcion/{id_inscripcion}", response_model=List[RespActividadRead], operation_id="listar_respuestas_inscripcion")
def listar_respuestas_inscripcion(
    id_inscripcion: int, 
    db: Session = Depends(get_db), 
    current_user: Usuario = Depends(get_current_user)
):
    return listar_por_inscripcion(db, RespActividad, id_inscripcion)

# =============================================================================
# 🔹 CALIFICACIONES + CÁLCULO DE NOTA FINAL
# =============================================================================

@router.post("/calificaciones", response_model=CalificacionRead, status_code=status.HTTP_201_CREATED, operation_id="registrar_calificacion")
def registrar_calificacion_endpoint(
    data: CalificacionCreate, 
    db: Session = Depends(get_db), 
    current_user: Usuario = Depends(require_role("DOCENTE", "ADMIN"))
):
    return crear_calificacion(db, data)

@router.post("/calificaciones/{id_inscripcion}/calcular-final", operation_id="calcular_nota_final")
def calcular_nota_final_endpoint(
    id_inscripcion: int, 
    db: Session = Depends(get_db), 
    current_user: Usuario = Depends(require_role("ADMIN", "DOCENTE"))
):
    nota = calcular_nota_final(db, id_inscripcion)
    return {"id_inscripcion": id_inscripcion, "nota_final": float(nota)}

# =============================================================================
# 🔹 ASISTENCIA
# =============================================================================

@router.post("/asistencia", response_model=AsistenciaRead, status_code=status.HTTP_201_CREATED, operation_id="registrar_asistencia")
def registrar_asistencia_endpoint(
    data: AsistenciaCreate, 
    db: Session = Depends(get_db), 
    current_user: Usuario = Depends(require_role("DOCENTE", "ADMIN"))
):
    return crear_asistencia(db, data)

@router.get("/asistencia/inscripcion/{id_inscripcion}", response_model=List[AsistenciaRead], operation_id="listar_asistencia_inscripcion")
def listar_asistencia_inscripcion(
    id_inscripcion: int, 
    db: Session = Depends(get_db), 
    current_user: Usuario = Depends(get_current_user)
):
    return listar_por_inscripcion(db, Asistencia, id_inscripcion)

# =============================================================================
# 🔹 CERTIFICADOS
# =============================================================================

@router.post("/certificados/generar/{id_inscripcion}", response_model=CertificadoRead, operation_id="generar_certificado")
def generar_certificado_endpoint(
    id_inscripcion: int, 
    db: Session = Depends(get_db), 
    current_user: Usuario = Depends(require_role("ADMIN", "COORDINADOR"))
):
    return generar_certificado(db, id_inscripcion)

@router.get("/certificados/{id_certificado}", response_model=CertificadoRead, operation_id="obtener_certificado")
def obtener_certificado_endpoint(
    id_certificado: int, 
    db: Session = Depends(get_db), 
    current_user: Usuario = Depends(get_current_user)
):
    result = _obtener(db, Certificado, id_certificado)
    if not result:
        raise HTTPException(status_code=404, detail="Certificado no encontrado")
    return result

# =============================================================================
# 🔹 ENCUESTA DE SATISFACCIÓN
# =============================================================================

@router.post("/encuestas", response_model=EncuestaSatisfaccionRead, status_code=status.HTTP_201_CREATED, operation_id="enviar_encuesta")
def enviar_encuesta_endpoint(
    data: EncuestaSatisfaccionCreate, 
    db: Session = Depends(get_db), 
    current_user: Usuario = Depends(get_current_user)
):
    # Validar que el estudiante solo encueste su propia inscripción
    from app.modules.enrollment.models.inscripcion import Inscripcion
    insc = db.get(Inscripcion, data.id_inscripcion)
    if not insc:
        raise HTTPException(status_code=404, detail="Inscripción no encontrada")
    return crear_encuesta(db, data)