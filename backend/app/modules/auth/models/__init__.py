# app/modules/auth/models/__init__.py
from .rol import Rol
from .usuario import Usuario
from .instancia import Instancia
from .log_auditoria import LogAuditoria
# ❌ QUITAR: from .estudiante import Estudiante
# ❌ QUITAR: from .docente import Docente
# ❌ QUITAR: from .portafolio import Portafolio

__all__ = ["Rol", "Usuario", "Instancia", "LogAuditoria"]