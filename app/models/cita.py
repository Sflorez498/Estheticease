"""
Modelo para representar citas en el sistema
Este modelo define la estructura completa de una cita en el salón de belleza
"""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .base import Base

class Cita(Base):
    """
    Modelo de Cita
    Representa una cita en el sistema de gestión de citas
    """
    __tablename__ = "citas"  # Nombre de la tabla en la base de datos

    # Definición de campos de la tabla
    id_cita = Column(Integer, primary_key=True, index=True)  # ID único de la cita
    id_cliente = Column(Integer, ForeignKey("clientes.Id_Cliente"))  # ID del cliente que hace la cita
    id_servicio = Column(Integer, ForeignKey("servicios.id_servicio"))  # ID del servicio solicitado
    fecha = Column(DateTime, nullable=False)  # Fecha y hora de la cita
    estado = Column(String(20), nullable=False)  # Estado actual de la cita (Pendiente, Confirmada, Cancelada, Completada)
    created_at = Column(DateTime, server_default=func.now())  # Fecha de creación de la cita
    updated_at = Column(DateTime, onupdate=func.now())  # Fecha de última actualización
    
    # Definición de relaciones con otras tablas
    cliente = relationship("Cliente", back_populates="citas")  # Relación con la tabla Clientes
    servicio = relationship("Servicio", back_populates="citas")  # Relación con la tabla Servicios
    
    def __repr__(self):
        """
        Representación en string del objeto Cita
        Muestra el ID, nombre del cliente y nombre del servicio
        """
        return f"Cita(id={self.id_cita}, cliente={self.cliente.nombre}, servicio={self.servicio.nombre})"
