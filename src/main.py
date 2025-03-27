from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routes.auth import router as login_router

app = FastAPI()

app.include_router(login_router, prefix="/login")

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Permite peticiones desde Vite
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permite todos los headers
)

@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI!"}
