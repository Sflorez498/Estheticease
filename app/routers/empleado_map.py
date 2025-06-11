from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from app.database.Clever_MySQL_conn import cleverCursor, mysqlConn
from typing import List, Optional
from datetime import datetime

class EmpleadoBase(BaseModel):
    nombre: str
    apellido: str
    email: str
    telefono: str
    direccion: str
    fecha_contratacion: datetime
    salario: float
    cargo: str

class Empleado(EmpleadoBase):
    id_empleado: Optional[int] = None

empleadoRouter = APIRouter()

@empleadoRouter.get("/", status_code=status.HTTP_200_OK)
async def listar_empleados():
    try:
        cleverCursor.execute('SELECT * FROM empleados')
        empleados = cleverCursor.fetchall()
        return empleados
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener empleados: {e}")

@empleadoRouter.get("/{empleado_id}", status_code=status.HTTP_200_OK)
async def obtener_empleado(empleado_id: int):
    try:
        cleverCursor.execute('SELECT * FROM empleados WHERE Id_Empleado = %s', (empleado_id,))
        empleado = cleverCursor.fetchone()
        if empleado:
            return empleado
        raise HTTPException(status_code=404, detail="Empleado no encontrado")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener empleado: {e}")

@empleadoRouter.post("/", status_code=status.HTTP_201_CREATED)
async def crear_empleado(empleado: EmpleadoBase):
    try:
        insert_query = """
        INSERT INTO empleados (Nombre, Apellido, Email, Telefono, Direccion, 
                             Fecha_Contratacion, Salario, Cargo)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (
            empleado.nombre,
            empleado.apellido,
            empleado.email,
            empleado.telefono,
            empleado.direccion,
            empleado.fecha_contratacion,
            empleado.salario,
            empleado.cargo
        )
        cleverCursor.execute(insert_query, values)
        mysqlConn.commit()
        return {"message": "Empleado creado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al crear empleado: {e}")

@empleadoRouter.put("/{empleado_id}", status_code=status.HTTP_200_OK)
async def actualizar_empleado(empleado_id: int, empleado: EmpleadoBase):
    try:
        update_query = """
        UPDATE empleados 
        SET Nombre = %s, Apellido = %s, Email = %s, Telefono = %s,
            Direccion = %s, Fecha_Contratacion = %s, Salario = %s, Cargo = %s
        WHERE Id_Empleado = %s
        """
        values = (
            empleado.nombre,
            empleado.apellido,
            empleado.email,
            empleado.telefono,
            empleado.direccion,
            empleado.fecha_contratacion,
            empleado.salario,
            empleado.cargo,
            empleado_id
        )
        cleverCursor.execute(update_query, values)
        mysqlConn.commit()
        return {"message": "Empleado actualizado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al actualizar empleado: {e}")

@empleadoRouter.delete("/{empleado_id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_empleado(empleado_id: int):
    try:
        cleverCursor.execute('DELETE FROM empleados WHERE Id_Empleado = %s', (empleado_id,))
        mysqlConn.commit()
        return {"message": "Empleado eliminado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al eliminar empleado: {e}") 