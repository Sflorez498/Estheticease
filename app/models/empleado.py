# Modelos de Empleados
# Estos modelos definen la estructura de los datos relacionados con los empleados

from pydantic import BaseModel, EmailStr
from typing import Optional

class EmpleadoBase(BaseModel):
    """
    Modelo base para empleados
    Contiene los campos comunes que se usan en todas las operaciones
    """
    nombre: str  # Nombre completo del empleado
    contacto: str  # Número de teléfono o contacto
    correo: EmailStr  # Email del empleado (validado)
    id_rol: int  # ID del rol del empleado (ej: administrador, estilista, etc.)

class EmpleadoCreate(EmpleadoBase):
    """
    Modelo para crear nuevos empleados
    Extiende de EmpleadoBase y agrega el campo contraseña
    """
    contraseña: str  # Contraseña del empleado

class EmpleadoUpdate(BaseModel):
    """
    Modelo para actualizar empleados existentes
    Todos los campos son opcionales para permitir actualizaciones parciales
    """
    nombre: Optional[str] = None  # Nombre del empleado (opcional)
    contacto: Optional[str] = None  # Contacto (opcional)
    correo: Optional[EmailStr] = None  # Email (opcional)
    id_rol: Optional[int] = None  # ID del rol (opcional)
    contraseña: Optional[str] = None  # Contraseña (opcional)

class Empleado(EmpleadoBase):
    """
    Modelo completo de empleado
    Incluye el ID del empleado y hereda los campos base
    """
    id_empleado: int  # ID único del empleado

    class Config:
        """
        Configuración del modelo
        Permite la conversión automática de objetos SQLAlchemy a Pydantic
        """
        from_attributes = True 