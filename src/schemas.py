from pydantic import BaseModel, EmailStr
from typing import Optional

class RolBase(BaseModel):
    nombre_rol: str   # <--- Mismo nombre que en la base de datos

class RolRead(RolBase):
    id_rol: int

    class Config:
        from_attributes = True

class UsuarioBase(BaseModel):
    nombre: str
    email: EmailStr

class UsuarioCreate(UsuarioBase):
    password: str
    id_rol: Optional[int] = 2

class UsuarioRead(UsuarioBase):
    id_usuario: int
    rol: Optional[RolRead]

    class Config:
        from_attributes = True
