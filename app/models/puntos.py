"""
Modelo para el sistema de puntos de fidelidad

Este modelo maneja los puntos acumulados por los clientes
y su historial de canjes.
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .base import Base

class Puntos(Base):
    """Modelo de Puntos de Fidelidad"""
    __tablename__ = "puntos"

    id_puntos = Column(Integer, primary_key=True, index=True)
    id_cliente = Column(Integer, ForeignKey("clientes.Id_Cliente"))
    puntos_acumulados = Column(Integer, nullable=False, default=0)
    puntos_restantes = Column(Integer, nullable=False, default=0)
    fecha_actualizacion = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    # Relaciones
    cliente = relationship("Cliente", back_populates="puntos")
    canjes = relationship("Canje", back_populates="puntos")

class Canje(Base):
    """Modelo de Canjes de Puntos"""
    __tablename__ = "canjes"

    id_canje = Column(Integer, primary_key=True, index=True)
    id_puntos = Column(Integer, ForeignKey("puntos.id_puntos"))
    puntos_canjeados = Column(Integer, nullable=False)
    premio = Column(String(100), nullable=False)
    fecha_canje = Column(DateTime, server_default=func.now())
    
    # Relaciones
    puntos = relationship("Puntos", back_populates="canjes")
