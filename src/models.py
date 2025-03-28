from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from src.database import Base

class Rol(Base):
    __tablename__ = "roles"

    id_rol = Column(Integer, primary_key=True, index=True)
    nombre_rol = Column(String, nullable=False)  # 👈 Nombre corregido

    usuarios = relationship("Usuario", back_populates="rol")  # Relación con Usuario

class Usuario(Base):
    __tablename__ = "usuarios"

    id_usuario = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    id_rol = Column(Integer, ForeignKey("roles.id_rol"), nullable=False)

    rol = relationship("Rol", back_populates="usuarios")  # Relación con Rol
