# Modelos para productos
# Estos modelos definen la estructura de los productos en el sistema

from pydantic import BaseModel
from typing import Optional
from decimal import Decimal

class ProductoBase(BaseModel):
    """
    Modelo base para productos
    Contiene los campos comunes que se usan en todas las operaciones
    """
    nombre_producto: str  # Nombre del producto
    categoria: str  # Categoría a la que pertenece (ej: cuidado facial, maquillaje, etc.)
    inventario: int  # Cantidad disponible en stock
    precio: Decimal  # Precio del producto (usa Decimal para precisión en cálculos)

class ProductoCreate(ProductoBase):
    """
    Modelo para crear nuevos productos
    Extiende de ProductoBase y usa la misma estructura
    """
    pass

class ProductoUpdate(BaseModel):
    """
    Modelo para actualizar productos existentes
    Todos los campos son opcionales para permitir actualizaciones parciales
    """
    nombre_producto: Optional[str] = None  # Nombre del producto (opcional)
    categoria: Optional[str] = None  # Categoría (opcional)
    inventario: Optional[int] = None  # Cantidad en stock (opcional)
    precio: Optional[Decimal] = None  # Precio (opcional)

class Producto(ProductoBase):
    """
    Modelo completo de producto
    Incluye el ID del producto y hereda los campos base
    """
    id_producto: int  # ID único del producto

    class Config:
        """
        Configuración del modelo
        Permite la conversión automática de objetos SQLAlchemy a Pydantic
        """
        from_attributes = True