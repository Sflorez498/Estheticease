from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database.database import get_db
from app.models.empleado import EmpleadoCreate, EmpleadoUpdate, Empleado
from app.models.producto import ProductoCreate, ProductoUpdate, Producto
from passlib.context import CryptContext
from app.auth.auth import get_current_admin_user

router = APIRouter(prefix="/admin", tags=["admin"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Rutas para gestión de empleados
@router.post("/empleados/", response_model=Empleado)
async def crear_empleado(empleado: EmpleadoCreate, db: Session = Depends(get_db), current_admin: dict = Depends(get_current_admin_user)):
    db_empleado = db.query(Empleado).filter(Empleado.correo == empleado.correo).first()
    if db_empleado:
        raise HTTPException(status_code=400, detail="El correo ya está registrado")
    
    hashed_password = pwd_context.hash(empleado.contraseña)
    nuevo_empleado = Empleado(**empleado.dict(exclude={'contraseña'}), contraseña=hashed_password)
    
    db.add(nuevo_empleado)
    db.commit()
    db.refresh(nuevo_empleado)
    return nuevo_empleado

@router.get("/empleados/", response_model=List[Empleado])
async def listar_empleados(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_admin: dict = Depends(get_current_admin_user)):
    empleados = db.query(Empleado).offset(skip).limit(limit).all()
    return empleados

@router.put("/empleados/{empleado_id}", response_model=Empleado)
async def actualizar_empleado(empleado_id: int, empleado: EmpleadoUpdate, db: Session = Depends(get_db), current_admin: dict = Depends(get_current_admin_user)):
    db_empleado = db.query(Empleado).filter(Empleado.id_empleado == empleado_id).first()
    if not db_empleado:
        raise HTTPException(status_code=404, detail="Empleado no encontrado")
    
    update_data = empleado.dict(exclude_unset=True)
    if "contraseña" in update_data:
        update_data["contraseña"] = pwd_context.hash(update_data["contraseña"])
    
    for key, value in update_data.items():
        setattr(db_empleado, key, value)
    
    db.commit()
    db.refresh(db_empleado)
    return db_empleado

# Rutas para gestión de productos
@router.post("/productos/", response_model=Producto)
async def crear_producto(producto: ProductoCreate, db: Session = Depends(get_db), current_admin: dict = Depends(get_current_admin_user)):
    nuevo_producto = Producto(**producto.dict())
    db.add(nuevo_producto)
    db.commit()
    db.refresh(nuevo_producto)
    return nuevo_producto

@router.get("/productos/", response_model=List[Producto])
async def listar_productos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_admin: dict = Depends(get_current_admin_user)):
    productos = db.query(Producto).offset(skip).limit(limit).all()
    return productos

@router.put("/productos/{producto_id}", response_model=Producto)
async def actualizar_producto(producto_id: int, producto: ProductoUpdate, db: Session = Depends(get_db), current_admin: dict = Depends(get_current_admin_user)):
    db_producto = db.query(Producto).filter(Producto.id_producto == producto_id).first()
    if not db_producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    update_data = producto.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_producto, key, value)
    
    db.commit()
    db.refresh(db_producto)
    return db_producto

@router.delete("/productos/{producto_id}")
async def eliminar_producto(producto_id: int, db: Session = Depends(get_db), current_admin: dict = Depends(get_current_admin_user)):
    db_producto = db.query(Producto).filter(Producto.id_producto == producto_id).first()
    if not db_producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    db.delete(db_producto)
    db.commit()
    return {"message": "Producto eliminado exitosamente"} 