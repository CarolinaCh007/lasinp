from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.usuario import Usuario, Rol, Instancia
from app.schemas.usuario import UsuarioCreate, LoginRequest, TokenResponse, UsuarioResponse
from passlib.context import CryptContext
from datetime import datetime, timedelta
import jwt
import os

router = APIRouter(prefix="/auth", tags=["Autenticación"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

def create_token(data: dict) -> str:
    payload = data.copy()
    payload["exp"] = datetime.utcnow() + timedelta(minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30)))
    return jwt.encode(payload, os.getenv("SECRET_KEY"), algorithm=os.getenv("ALGORITHM"))

@router.post("/registro", response_model=UsuarioResponse)
def registro(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    # Verificar si el correo ya existe
    existe = db.query(Usuario).filter(Usuario.correo_electronico == usuario.correo_electronico).first()
    if existe:
        raise HTTPException(status_code=400, detail="El correo ya está registrado")
    
    # Crear usuario con contraseña encriptada
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
    # Buscar usuario por correo
    usuario = db.query(Usuario).filter(Usuario.correo_electronico == datos.correo_electronico).first()
    if not usuario:
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")
    
    # Verificar contraseña
    if not verify_password(datos.password, usuario.password):
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")
    
    # Verificar estado
    if usuario.estado == "bloqueado":
        raise HTTPException(status_code=403, detail="Usuario bloqueado")
    if usuario.estado == "inactivo":
        raise HTTPException(status_code=403, detail="Usuario inactivo")
    
    # Obtener rol
    instancia = db.query(Instancia).filter(Instancia.id_usuario == usuario.id_usuario).first()
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