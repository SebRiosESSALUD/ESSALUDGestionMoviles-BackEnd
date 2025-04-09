from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload  # <-- Importar selectinload
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta

from src.database import get_db
from src.models import Usuario, Rol
from src.schemas import UsuarioCreate, UsuarioRead
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

SECRET_KEY = "TU_CLAVE_SECRETA"  # En producción, usa variables de entorno
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

    result = await db.execute(
        select(Usuario).options(selectinload(Usuario.rol)).filter(Usuario.email == email)
    )
    user = result.scalar()
    if user is None:
        raise credentials_exception
    return user

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Usuario)
        .options(selectinload(Usuario.rol))  # <-- Cargar la relación 'rol' de forma anticipada
        .filter(Usuario.email == form_data.username)
    )
    user = result.scalar()
    
    if not user or not pwd_context.verify(form_data.password, user.password_hash):
        raise HTTPException(status_code=400, detail="Credenciales incorrectas")

    access_token = create_access_token(data={"sub": user.email})
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "id_rol": user.id_rol,
        "nombre_rol": user.rol.nombre_rol  # Ahora la relación 'rol' ya viene precargada
    }

@router.get("/me", response_model=UsuarioRead)
async def read_users_me(current_user: Usuario = Depends(get_current_user)):
    """
    Devuelve la información del usuario autenticado.
    """
    return current_user
