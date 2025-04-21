from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.database import engine, Base
from src.routes.auth import router as usuarios_router
from src.crud import devices_router, operadoras_router, modelos_router

app = FastAPI()

# Aquí se configura la creación de tablas al arrancar el servidor
@app.on_event("startup")
async def on_startup():
    # Ejecutar DDL de forma asíncrona para crear las tablas definidas en los modelos
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Rutas
# (Las tablas ya se crean en on_startup)

app.include_router(usuarios_router)
app.include_router(devices_router)
app.include_router(operadoras_router)
app.include_router(modelos_router)

# Configuración de CORS
tija = app  # alias para evitar confusión con nombre de variable
tija.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar orígenes reales
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI!"}
