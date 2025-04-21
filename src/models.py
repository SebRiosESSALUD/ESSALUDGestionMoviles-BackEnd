from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from src.database import Base

class Rol(Base):
    __tablename__ = "roles"

    id_rol = Column(Integer, primary_key=True, index=True)
    nombre_rol = Column(String, nullable=False)

    usuarios = relationship("Usuario", back_populates="rol")


class Usuario(Base):
    __tablename__ = "usuarios"

    id_usuario   = Column(Integer, primary_key=True, index=True)
    nombre       = Column(String, nullable=False)
    email        = Column(String, unique=True, nullable=False)
    password_hash= Column(String, nullable=False)
    id_rol       = Column(Integer, ForeignKey("roles.id_rol"), nullable=False)

    rol = relationship("Rol", back_populates="usuarios")


class Operadora(Base):
    __tablename__ = "operadoras"

    id_operadora   = Column(Integer, primary_key=True, index=True)
    nombre         = Column("nombre", String, unique=True, nullable=False)

    moviles        = relationship("Movil", back_populates="operadora")


class ModeloMovil(Base):
    __tablename__ = "modelos_moviles"

    id_modelo        = Column(Integer, primary_key=True, index=True)
    nombre           = Column("nombre", String, unique=True, nullable=False)
    marca            = Column(String, nullable=False)
    año_fabricacion  = Column(Integer, nullable=True)

    moviles          = relationship("Movil", back_populates="modelo")


class Movil(Base):
    __tablename__ = "moviles"

    id_movil      = Column(Integer, primary_key=True, index=True)
    numero        = Column(String, unique=True, nullable=False)
    id_operadora  = Column(Integer, ForeignKey("operadoras.id_operadora"), nullable=False)
    id_modelo     = Column(Integer, ForeignKey("modelos_moviles.id_modelo"), nullable=False)

    operadora     = relationship("Operadora", back_populates="moviles")
    modelo        = relationship("ModeloMovil", back_populates="moviles")


class HistorialCambios(Base):
    __tablename__ = "historial_cambios"

    id_historial   = Column(Integer, primary_key=True, index=True)
    fecha          = Column(DateTime, nullable=False)
    tipo_cambio    = Column(String, nullable=False)
    motivo         = Column(Text, nullable=True)
    id_trabajador  = Column(Integer, ForeignKey("usuarios.id_usuario"), nullable=False)
    id_movil       = Column(Integer, ForeignKey("moviles.id_movil"), nullable=False)

    movil          = relationship("Movil")
    trabajador     = relationship("Usuario")
