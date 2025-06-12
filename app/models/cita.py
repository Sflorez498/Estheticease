"""
Modelo para representar citas en el sistema

Este modelo define la estructura de las citas, incluyendo
la información del cliente, el servicio, la fecha y estado.
"""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .base import Base

class Cita(Base):
    """Modelo de Cita"""
    __tablename__ = "citas"

    id_cita = Column(Integer, primary_key=True, index=True)
    id_cliente = Column(Integer, ForeignKey("clientes.Id_Cliente"))
    id_servicio = Column(Integer, ForeignKey("servicios.id_servicio"))
    fecha = Column(DateTime, nullable=False)
    estado = Column(String(20), nullable=False)  # Pendiente, Confirmada, Cancelada, Completada
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    
    # Relaciones
    cliente = relationship("Cliente", back_populates="citas")
    servicio = relationship("Servicio", back_populates="citas")
    
    def __repr__(self):
        return f"Cita(id={self.id_cita}, cliente={self.cliente.nombre}, servicio={self.servicio.nombre})"
