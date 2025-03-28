from pydantic import BaseModel, EmailStr
from typing import Optional

class RolBase(BaseModel):
    nombre: str

class RolRead(RolBase):
    id_rol: int

    class Config:
        from_attributes = True  # Permite mapear desde SQLAlchemy a Pydantic

class UsuarioBase(BaseModel):
    nombre: str
    email: EmailStr

class UsuarioCreate(UsuarioBase):
    password: str
    id_rol: Optional[int] = 2  # Por defecto, asignamos el rol 2 (ejemplo: usuario normal)

class UsuarioRead(UsuarioBase):
    id_usuario: int
    rol: Optional[RolRead]  # Para incluir detalles del rol al leer usuarios

    class Config:
        from_attributes = True
