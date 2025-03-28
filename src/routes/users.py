from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.models import User
from src.schemas import UserCreate
from src.database import get_db
from src.utils.security import hash_password

router = APIRouter()

@router.post("/usuarios/admin")
async def create_admin(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    # Verificar si el usuario ya existe
    result = await db.execute(select(User).filter(User.email == user_data.email))
    existing_user = result.scalar()

    if existing_user:
        raise HTTPException(status_code=400, detail="El usuario ya existe")

    # Crear usuario con contraseña hasheada
    hashed_password = hash_password(user_data.password)
    new_user = User(
        nombre=user_data.nombre,
        email=user_data.email,
        password_hash=hashed_password,
        id_rol=1  # Asigna el rol de administrador
    )

    db.add(new_user)
    await db.commit()
    return {"message": f"Administrador {user_data.email} creado exitosamente"}
