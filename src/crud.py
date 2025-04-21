from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError

from src.database import get_db
from src.models import Movil, Operadora, ModeloMovil, HistorialCambios, Usuario
from src.schemas import (
    MovilCreate, MovilRead, MovilUpdate,
    OperadoraRead, OperadoraCreate,
    ModeloMovilRead, ModeloMovilCreate,
    HistorialCambiosCreate, HistorialCambiosRead
)
from src.routes.auth import get_current_user

# IDs de roles
ADMIN_ROLE_ID  = 1
GESTOR_ROLE_ID = 2

devices_router      = APIRouter(prefix="/moviles", tags=["Moviles"])
operadoras_router   = APIRouter(prefix="/operadoras", tags=["Operadoras"])
modelos_router      = APIRouter(prefix="/modelos", tags=["Modelos"])
historial_router    = APIRouter(prefix="/historial", tags=["Historial Cambios"])


# ——— Moviles ———
@devices_router.get("/", response_model=list[MovilRead])
async def list_moviles(db: AsyncSession = Depends(get_db),
                       current_user: Usuario = Depends(get_current_user)):
    result = await db.execute(select(Movil))
    return result.scalars().all()

@devices_router.post("/", response_model=MovilRead, status_code=status.HTTP_201_CREATED)
async def create_movil(data: MovilCreate,
                       db: AsyncSession = Depends(get_db),
                       current_user: Usuario = Depends(get_current_user)):
    if current_user.id_rol not in (ADMIN_ROLE_ID, GESTOR_ROLE_ID):
        raise HTTPException(403, "No tienes permiso para crear moviles")
    m = Movil(**data.dict())
    db.add(m)
    try:
        await db.commit()
        await db.refresh(m)
    except IntegrityError:
        await db.rollback()
        raise HTTPException(400, "Número duplicado o clave inválida")
    return m

@devices_router.put("/{id_movil}", response_model=MovilRead)
async def update_movil(id_movil: int, data: MovilUpdate,
                       db: AsyncSession = Depends(get_db),
                       current_user: Usuario = Depends(get_current_user)):
    if current_user.id_rol not in (ADMIN_ROLE_ID, GESTOR_ROLE_ID):
        raise HTTPException(403, "No tienes permiso para modificar moviles")
    res = await db.execute(select(Movil).filter(Movil.id_movil == id_movil))
    m = res.scalar_one_or_none()
    if not m:
        raise HTTPException(404, "Movil no encontrado")
    for k, v in data.dict(exclude_unset=True).items():
        setattr(m, k, v)
    await db.commit()
    await db.refresh(m)
    return m

@devices_router.delete("/{id_movil}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_movil(id_movil: int,
                       db: AsyncSession = Depends(get_db),
                       current_user: Usuario = Depends(get_current_user)):
    if current_user.id_rol != ADMIN_ROLE_ID:
        raise HTTPException(403, "No tienes permiso para eliminar moviles")
    res = await db.execute(select(Movil).filter(Movil.id_movil == id_movil))
    m = res.scalar_one_or_none()
    if not m:
        raise HTTPException(404, "Movil no encontrado")
    await db.delete(m)
    await db.commit()


# ——— Operadoras ———
@operadoras_router.get("/", response_model=list[OperadoraRead])
async def list_operadoras(db: AsyncSession = Depends(get_db),
                          current_user: Usuario = Depends(get_current_user)):
    res = await db.execute(select(Operadora))
    return res.scalars().all()

@operadoras_router.post("/", response_model=OperadoraRead, status_code=status.HTTP_201_CREATED)
async def create_operadora(data: OperadoraCreate,
                           db: AsyncSession = Depends(get_db),
                           current_user: Usuario = Depends(get_current_user)):
    if current_user.id_rol not in (ADMIN_ROLE_ID, GESTOR_ROLE_ID):
        raise HTTPException(403, "No tienes permiso para crear operadoras")
    op = Operadora(nombre=data.nombre)
    db.add(op)
    try:
        await db.commit()
        await db.refresh(op)
    except IntegrityError:
        await db.rollback()
        raise HTTPException(400, "Operadora duplicada")
    return op


# ——— Modelos ———
@modelos_router.get("/", response_model=list[ModeloMovilRead])
async def list_modelos(db: AsyncSession = Depends(get_db),
                       current_user: Usuario = Depends(get_current_user)):
    res = await db.execute(select(ModeloMovil))
    return res.scalars().all()

@modelos_router.post("/", response_model=ModeloMovilRead, status_code=status.HTTP_201_CREATED)
async def create_modelo(data: ModeloMovilCreate,
                        db: AsyncSession = Depends(get_db),
                        current_user: Usuario = Depends(get_current_user)):
    if current_user.id_rol not in (ADMIN_ROLE_ID, GESTOR_ROLE_ID):
        raise HTTPException(403, "No tienes permiso para crear modelos")
    m = ModeloMovil(**data.dict())
    db.add(m)
    try:
        await db.commit()
        await db.refresh(m)
    except IntegrityError:
        await db.rollback()
        raise HTTPException(400, "Modelo duplicado")
    return m


# ——— Historial Cambios ———
@historial_router.get("/", response_model=list[HistorialCambiosRead])
async def list_historial(db: AsyncSession = Depends(get_db),
                         current_user: Usuario = Depends(get_current_user)):
    res = await db.execute(select(HistorialCambios))
    return res.scalars().all()

@historial_router.post("/", response_model=HistorialCambiosRead, status_code=status.HTTP_201_CREATED)
async def create_historial(data: HistorialCambiosCreate,
                           db: AsyncSession = Depends(get_db),
                           current_user: Usuario = Depends(get_current_user)):
    if current_user.id_rol not in (ADMIN_ROLE_ID, GESTOR_ROLE_ID):
        raise HTTPException(403, "No tienes permiso para registrar historial")
    h = HistorialCambios(**data.dict())
    db.add(h)
    await db.commit()
    await db.refresh(h)
    return h
