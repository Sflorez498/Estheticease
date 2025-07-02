"""
Modelo para el sistema de puntos de fidelidad
Este sistema permite a los clientes acumular puntos por sus compras y servicios
y canjearlos por premios especiales
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .base import Base

class Puntos(Base):
    """
    Modelo de Puntos de Fidelidad
    Representa el estado actual de los puntos de un cliente
    """
    __tablename__ = "puntos"  # Nombre de la tabla en la base de datos

    # Definición de campos
    id_puntos = Column(Integer, primary_key=True, index=True)  # ID único del registro de puntos
    id_cliente = Column(Integer, ForeignKey("clientes.Id_Cliente"))  # ID del cliente asociado
    puntos_acumulados = Column(Integer, nullable=False, default=0)  # Total de puntos acumulados
    puntos_restantes = Column(Integer, nullable=False, default=0)  # Puntos disponibles para canjear
    fecha_actualizacion = Column(DateTime, server_default=func.now(), onupdate=func.now())  # Fecha de última actualización
    
    # Definición de relaciones
    cliente = relationship("Cliente", back_populates="puntos")  # Relación con el cliente
    canjes = relationship("Canje", back_populates="puntos")  # Relación con los canjes realizados

class Canje(Base):
    """
    Modelo de Canjes de Puntos
    Representa un canje realizado por un cliente
    """
    __tablename__ = "canjes"  # Nombre de la tabla en la base de datos

    # Definición de campos
    id_canje = Column(Integer, primary_key=True, index=True)  # ID único del canje
    id_puntos = Column(Integer, ForeignKey("puntos.id_puntos"))  # ID del registro de puntos
    puntos_canjeados = Column(Integer, nullable=False)  # Cantidad de puntos canjeados
    premio = Column(String(100), nullable=False)  # Descripción del premio obtenido
    fecha_canje = Column(DateTime, server_default=func.now())  # Fecha del canje
    
    # Definición de relaciones
    puntos = relationship("Puntos", back_populates="canjes")  # Relación con el registro de puntos
