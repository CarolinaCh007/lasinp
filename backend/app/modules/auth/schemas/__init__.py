from .auth import (
    Token,
    LoginRequest,
    ChangePasswordRequest,
    StudentRegisterRequest,
    TeacherCreateRequest,
    AdminCreateRequest,
    EmailVerificationResponse,
    PasswordResetRequest,
    PasswordResetConfirm,
    LoginResponse,  # ← Agregar este
    UserInfo,       # ← Opcional: si quieres usarlos por separado
    RoleInfo,
    InstanceInfo
)

__all__ = [
    "Token", "LoginRequest", "ChangePasswordRequest",
    "StudentRegisterRequest", "TeacherCreateRequest", "AdminCreateRequest",
    "EmailVerificationResponse", "PasswordResetRequest", "PasswordResetConfirm",
    "LoginResponse", "UserInfo", "RoleInfo", "InstanceInfo"  # ← Agregar estos
]