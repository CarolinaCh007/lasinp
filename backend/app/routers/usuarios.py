from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.usuario import Usuario, Rol, Instancia
from app.models.estudiante import Estudiante
from app.models.docente import Docente
from app.schemas.usuario import UsuarioCreate, UsuarioResponse, UsuarioUpdate
from app.core.security import hash_password
from app.core.dependencies import require_rol
from datetime import datetime

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])

# ── GET todos los usuarios ────────────────────────────────
@router.get("/", response_model=List[UsuarioResponse])
def listar_usuarios(
    db: Session = Depends(get_db),
    _=Depends(require_rol("admin", "superadmin"))
):
    return db.query(Usuario).all()

# ── GET usuario por ID ────────────────────────────────────
@router.get("/{id_usuario}", response_model=UsuarioResponse)
def obtener_usuario(
    id_usuario: int,
    db: Session = Depends(get_db),
    _=Depends(require_rol("admin", "superadmin"))
):
    usuario = db.query(Usuario).filter(Usuario.id_usuario == id_usuario).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

# ── POST crear usuario ────────────────────────────────────
@router.post("/", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
def crear_usuario(
    usuario: UsuarioCreate,
    db: Session = Depends(get_db),
    _=Depends(require_rol("admin", "superadmin"))
):
    # Verificar correo duplicado
    if db.query(Usuario).filter(Usuario.correo_electronico == usuario.correo_electronico).first():
        raise HTTPException(status_code=400, detail="El correo ya está registrado")
    
    # Verificar CI duplicado
    if usuario.ci and db.query(Usuario).filter(Usuario.ci == usuario.ci).first():
        raise HTTPException(status_code=400, detail="El CI ya está registrado")

    nuevo = Usuario(
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
        estado="activo"
    )
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

# ── PUT actualizar usuario ────────────────────────────────
@router.put("/{id_usuario}", response_model=UsuarioResponse)
def actualizar_usuario(
    id_usuario: int,
    datos: UsuarioUpdate,
    db: Session = Depends(get_db),
    _=Depends(require_rol("admin", "superadmin"))
):
    usuario = db.query(Usuario).filter(Usuario.id_usuario == id_usuario).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    for campo, valor in datos.model_dump(exclude_unset=True).items():
        setattr(usuario, campo, valor)
    
    usuario.updated_at = datetime.now()
    db.commit()
    db.refresh(usuario)
    return usuario

# ── DELETE eliminar usuario ───────────────────────────────
@router.delete("/{id_usuario}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_usuario(
    id_usuario: int,
    db: Session = Depends(get_db),
    _=Depends(require_rol("superadmin"))
):
    usuario = db.query(Usuario).filter(Usuario.id_usuario == id_usuario).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    db.delete(usuario)
    db.commit()

# ── PATCH cambiar estado ──────────────────────────────────
@router.patch("/{id_usuario}/estado", response_model=UsuarioResponse)
def cambiar_estado(
    id_usuario: int,
    estado: str,
    db: Session = Depends(get_db),
    _=Depends(require_rol("admin", "superadmin"))
):
    estados_validos = ["activo", "inactivo", "pendiente", "bloqueado"]
    if estado not in estados_validos:
        raise HTTPException(status_code=400, detail=f"Estado inválido. Use: {estados_validos}")
    
    usuario = db.query(Usuario).filter(Usuario.id_usuario == id_usuario).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    usuario.estado = estado
    usuario.updated_at = datetime.now()
    db.commit()
    db.refresh(usuario)
    return usuario

# ── POST asignar rol ──────────────────────────────────────
@router.post("/{id_usuario}/rol", status_code=status.HTTP_201_CREATED)
def asignar_rol(
    id_usuario: int,
    id_rol: int,
    db: Session = Depends(get_db),
    _=Depends(require_rol("admin", "superadmin"))
):
    usuario = db.query(Usuario).filter(Usuario.id_usuario == id_usuario).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    rol = db.query(Rol).filter(Rol.id_rol == id_rol).first()
    if not rol:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    
    # Verificar si ya tiene ese rol
    existe = db.query(Instancia).filter(
        Instancia.id_usuario == id_usuario,
        Instancia.id_rol == id_rol
    ).first()
    if existe:
        raise HTTPException(status_code=400, detail="El usuario ya tiene ese rol")
    
    instancia = Instancia(id_usuario=id_usuario, id_rol=id_rol)
    db.add(instancia)
    db.commit()
    return {"mensaje": f"Rol {rol.nombre} asignado correctamente"}

# ── GET usuarios con su rol ───────────────────────────────
@router.get("/{id_usuario}/rol")
def obtener_rol_usuario(
    id_usuario: int,
    db: Session = Depends(get_db),
    _=Depends(require_rol("admin", "superadmin"))
):
    instancia = db.query(Instancia).filter(Instancia.id_usuario == id_usuario).first()
    if not instancia:
        return {"rol": "sin_rol"}
    rol = db.query(Rol).filter(Rol.id_rol == instancia.id_rol).first()
    return {"rol": rol.nombre if rol else "sin_rol"}