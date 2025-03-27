from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL = "postgresql+asyncpg://user:password@localhost/dbname"

engine = create_async_engine(DATABASE_URL, future=True, echo=True)
SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

async def get_db():
    async with SessionLocal() as session:
        yield session
