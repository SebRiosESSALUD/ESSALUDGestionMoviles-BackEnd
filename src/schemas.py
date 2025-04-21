from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class RolBase(BaseModel):
    nombre_rol: str

class RolRead(RolBase):
    id_rol: int
    class Config:
        orm_mode = True

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
        orm_mode = True

class OperadoraCreate(BaseModel):
    nombre: str

class OperadoraRead(BaseModel):
    id_operadora: int
    nombre: str
    class Config:
        orm_mode = True

class ModeloMovilCreate(BaseModel):
    nombre: str
    marca: str
    año_fabricacion: Optional[int]

class ModeloMovilRead(BaseModel):
    id_modelo: int
    nombre: str
    marca: str
    año_fabricacion: Optional[int]
    class Config:
        orm_mode = True

class MovilBase(BaseModel):
    numero: str
    id_operadora: int
    id_modelo: int

class MovilCreate(MovilBase):
    pass

class MovilUpdate(BaseModel):
    numero: Optional[str] = None
    id_operadora: Optional[int] = None
    id_modelo: Optional[int] = None

class MovilRead(MovilBase):
    id_movil: int
    class Config:
        orm_mode = True

class HistorialCambiosBase(BaseModel):
    fecha: datetime
    tipo_cambio: str
    motivo: Optional[str]
    id_trabajador: int
    id_movil: int

class HistorialCambiosCreate(HistorialCambiosBase):
    pass

class HistorialCambiosRead(HistorialCambiosBase):
    id_historial: int
    class Config:
        orm_mode = True
