from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta

from src.database import get_db
from src.models import Usuario, Rol
from src.schemas import UsuarioCreate, UsuarioRead
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

# Configuración de seguridad
SECRET_KEY = "TU_CLAVE_SECRETA"  # 🔴 Usa una variable de entorno en producción
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="usuarios/login")


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudo validar el token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    result = await db.execute(select(Usuario).filter(Usuario.email == email))
    user = result.scalar()
    if user is None:
        raise credentials_exception
    return user


@router.post("/admin")
async def create_admin(user_data: UsuarioCreate, db: AsyncSession = Depends(get_db)):
    # Verificar si el usuario ya existe
    result = await db.execute(select(Usuario).filter(Usuario.email == user_data.email))
    user = result.scalar()
    if user:
        raise HTTPException(status_code=400, detail="El usuario ya existe")

    # Validar que el id_rol proporcionado exista en la BD
    result = await db.execute(select(Rol).filter(Rol.id_rol == user_data.id_rol))
    rol = result.scalar()
    if not rol:
        raise HTTPException(status_code=400, detail="El rol especificado no existe")

    # Crear nuevo usuario con el rol especificado
    new_user = Usuario(
        email=user_data.email,
        password_hash=pwd_context.hash(user_data.password),
        nombre=user_data.nombre,
        id_rol=user_data.id_rol
    )

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    
    return {"message": "Usuario administrador creado exitosamente", "rol": rol.nombre_rol}


@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Usuario).filter(Usuario.email == form_data.username))
    user = result.scalar()
    
    if not user or not pwd_context.verify(form_data.password, user.password_hash):
        raise HTTPException(status_code=400, detail="Credenciales incorrectas")

    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=UsuarioRead)
async def read_users_me(current_user: Usuario = Depends(get_current_user)):
    return current_user
