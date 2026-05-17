from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import engine, Base
from app.core.config import settings

# =============================================================================
# 🔹 IMPORTAR MODELOS para registrar tablas en SQLAlchemy
# =============================================================================
from app.modules.auth import models as auth_models
from app.modules.academic import models as academic_models
from app.modules.courses import models as courses_models
from app.modules.scheduling import models as scheduling_models  # ← Nuevo módulo

# =============================================================================
# 🔹 Inicializar FastAPI
# =============================================================================
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="API para sistema educativo - Proyecto de Grado UMSA"
)

# =============================================================================
# 🔹 CORS: Permitir conexiones desde frontend
# =============================================================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =============================================================================
# 🔹 REGISTRAR ROUTERS - Módulo AUTH
# =============================================================================
from app.modules.auth.routers.auth_router import router as auth_router
from app.modules.auth.routers.usuario_router import router as usuario_router

app.include_router(auth_router, prefix="/api/v1", tags=["🔐 Autenticación"])
app.include_router(usuario_router, prefix="/api/v1", tags=["👥 Usuarios"])

# =============================================================================
# 🔹 REGISTRAR ROUTERS - Módulo ACADEMIC
# =============================================================================
from app.modules.academic.routers.estudiante_router import router as estudiante_router
from app.modules.academic.routers.docente_router import router as docente_router
from app.modules.academic.routers.portafolio_router import router as portafolio_router

app.include_router(estudiante_router, prefix="/api/v1", tags=["🎓 Académico"])
app.include_router(docente_router, prefix="/api/v1", tags=["🎓 Académico"])
app.include_router(portafolio_router, prefix="/api/v1", tags=["🎓 Académico"])

# =============================================================================
# 🔹 REGISTRAR ROUTERS - Módulo COURSES
# =============================================================================
from app.modules.courses.routers.curso_router import router as curso_router
from app.modules.courses.routers.tema_router import router as tema_router
from app.modules.courses.routers.ruta_aprendizaje_router import router as ruta_aprendizaje_router
from app.modules.courses.routers.ruta_tiene_router import router as ruta_tiene_router

app.include_router(curso_router, prefix="/api/v1", tags=["📚 Cursos"])
app.include_router(tema_router, prefix="/api/v1", tags=["📚 Cursos"])
app.include_router(ruta_aprendizaje_router, prefix="/api/v1", tags=["📚 Cursos"])
app.include_router(ruta_tiene_router, prefix="/api/v1", tags=["📚 Cursos"])

# =============================================================================
# 🔹 REGISTRAR ROUTERS - Módulo SCHEDULING (NUEVO)
# =============================================================================
from app.modules.scheduling.routers.aula_router import router as aula_router
from app.modules.scheduling.routers.horario_router import router as horario_router

app.include_router(aula_router, prefix="/api/v1", tags=["🏫 Scheduling"])
app.include_router(horario_router, prefix="/api/v1", tags=["🏫 Scheduling"])

# =============================================================================
# 🔹 Startup: Crear tablas (solo para desarrollo)
# =============================================================================
@app.on_event("startup")
def startup_event():
    """Crea tablas si no existen (solo para desarrollo)"""
    Base.metadata.create_all(bind=engine)

# =============================================================================
# 🔹 Endpoints Root y Health
# =============================================================================
@app.get("/", tags=["🏠 Root"])
def root():
    return {
        "message": "✅ Sistema Educativo API - Backend activo",
        "docs": "/docs",
        "health": "/health",
        "modules": ["auth", "academic", "courses", "scheduling"]
    }

@app.get("/health", tags=["🏠 Root"])
def health_check():
    return {"status": "ok", "database": "connected"}