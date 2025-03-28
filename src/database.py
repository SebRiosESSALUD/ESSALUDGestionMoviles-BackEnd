from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql+asyncpg://postgres:123456@localhost/gestor_moviles"

# Base para los modelos
Base = declarative_base()

# Configuración del motor de la base de datos
engine = create_async_engine(DATABASE_URL, echo=True)

# Sesión asincrónica
async_session_maker = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Función para obtener la sesión
async def get_db():
    async with async_session_maker() as session:
        yield session
