from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routes.auth import router as usuarios_router  # Cambié el alias para mayor claridad

app = FastAPI()

# Incluir rutas
app.include_router(usuarios_router)

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Cambiar esto solamente a las direcciones reales una vexz colocado en produccion
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permite todos los headers
)

@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI!"}
