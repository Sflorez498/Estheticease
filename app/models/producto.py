from pydantic import BaseModel
from typing import Optional
from decimal import Decimal

class ProductoBase(BaseModel):
    nombre_producto: str
    categoria: str
    inventario: int
    precio: Decimal

class ProductoCreate(ProductoBase):
    pass

class ProductoUpdate(BaseModel):
    nombre_producto: Optional[str] = None
    categoria: Optional[str] = None
    inventario: Optional[int] = None
    precio: Optional[Decimal] = None

class Producto(ProductoBase):
    id_producto: int

    class Config:
        from_attributes = True 