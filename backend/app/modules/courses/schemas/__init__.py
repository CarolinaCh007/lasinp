# =============================================================================
# 🔹 EXPORTS PARA SCHEMAS DEL MÓDULO COURSES
# =============================================================================

# Curso
from .curso import CursoCreate, CursoRead, CursoUpdate

# Tema
from .tema import TemaCreate, TemaRead, TemaUpdate

# RutaAprendizaje
from .ruta_aprendizaje import (
    RutaAprendizajeCreate, 
    RutaAprendizajeRead, 
    RutaAprendizajeUpdate
)

# RutaTiene
from .ruta_tiene import RutaTieneCreate, RutaTieneRead

# =============================================================================
# 🔹 __all__ para imports explícitos
# =============================================================================
__all__ = [
    # Curso
    "CursoCreate", "CursoRead", "CursoUpdate",
    # Tema
    "TemaCreate", "TemaRead", "TemaUpdate",
    # RutaAprendizaje
    "RutaAprendizajeCreate", "RutaAprendizajeRead", "RutaAprendizajeUpdate",
    # RutaTiene
    "RutaTieneCreate", "RutaTieneRead"
]