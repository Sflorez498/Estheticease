from pydantic import BaseModel, EmailStr
from typing import Optional

class EmpleadoBase(BaseModel):
    nombre: str
    contacto: str
    correo: EmailStr
    id_rol: int

class EmpleadoCreate(EmpleadoBase):
    contraseña: str

class EmpleadoUpdate(BaseModel):
    nombre: Optional[str] = None
    contacto: Optional[str] = None
    correo: Optional[EmailStr] = None
    id_rol: Optional[int] = None
    contraseña: Optional[str] = None

class Empleado(EmpleadoBase):
    id_empleado: int

    class Config:
        from_attributes = True 