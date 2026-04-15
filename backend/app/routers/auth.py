from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.usuario import Usuario, Rol, Instancia
from app.schemas.usuario import UsuarioCreate, LoginRequest, TokenResponse, UsuarioResponse
from app.core.security import hash_password, verify_password, create_token
from app.core.dependencies import get_current_user
from datetime import datetime

router = APIRouter(prefix="/auth", tags=["Autenticación"])

@router.post("/registro", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
def registro(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    # Verificar si el correo ya existe
    existe = db.query(Usuario).filter(
        Usuario.correo_electronico == usuario.correo_electronico
    ).first()
    if existe:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El correo ya está registrado"
        )

    # Verificar si el CI ya existe
    if usuario.ci:
        existe_ci = db.query(Usuario).filter(Usuario.ci == usuario.ci).first()
        if existe_ci:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El CI ya está registrado"
            )

    nuevo_usuario = Usuario(
        ci=usuario.ci,
        correo_electronico=usuario.correo_electronico,
        password=hash_password(usuario.password),
        nombre=usuario.nombre,
        ape_paterno=usuario.ape_paterno,
        ape_materno=usuario.ape_materno,
        celular=usuario.celular,
        fecha_nacimiento=usuario.fecha_nacimiento,
        direccion=usuario.direccion,
        sexo=usuario.sexo,
        estado="pendiente"
    )
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return nuevo_usuario

@router.post("/login", response_model=TokenResponse)
def login(datos: LoginRequest, db: Session = Depends(get_db)):
    # Buscar usuario
    usuario = db.query(Usuario).filter(
        Usuario.correo_electronico == datos.correo_electronico
    ).first()
    if not usuario or not verify_password(datos.password, usuario.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas"
        )

    # Verificar estado
    if usuario.estado == "bloqueado":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Usuario bloqueado")
    if usuario.estado == "inactivo":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Usuario inactivo")

    # Obtener rol
    instancia = db.query(Instancia).filter(
        Instancia.id_usuario == usuario.id_usuario
    ).first()
    rol = "sin_rol"
    if instancia:
        rol_obj = db.query(Rol).filter(Rol.id_rol == instancia.id_rol).first()
        if rol_obj:
            rol = rol_obj.nombre

    # Actualizar ultimo acceso
    usuario.ultimo_acceso = datetime.now()
    db.commit()

    # Crear token
    token = create_token({"sub": str(usuario.id_usuario), "rol": rol})

    return {
        "access_token": token,
        "token_type": "bearer",
        "usuario": usuario,
        "rol": rol
    }

@router.get("/me", response_model=UsuarioResponse)
def get_me(current_user: Usuario = Depends(get_current_user)):
    return current_user