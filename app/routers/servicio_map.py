from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from database.Clever_MySQL_conn import cleverCursor, mysqlConn
from typing import List, Optional

class ServicioBase(BaseModel):
    nombre: str
    descripcion: str
    precio: float

class Servicio(ServicioBase):
    id_servicio: Optional[int] = None

servicioRouter = APIRouter()

@servicioRouter.get("/", status_code=status.HTTP_200_OK)
async def listar_servicios():
    try:
        cleverCursor.execute('SELECT * FROM servicios')
        servicios = cleverCursor.fetchall()
        return servicios
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener servicios: {e}")

@servicioRouter.get("/{servicio_id}", status_code=status.HTTP_200_OK)
async def obtener_servicio(servicio_id: int):
    try:
        cleverCursor.execute('SELECT * FROM servicios WHERE Id_Servicio = %s', (servicio_id,))
        servicio = cleverCursor.fetchone()
        if servicio:
            return servicio
        raise HTTPException(status_code=404, detail="Servicio no encontrado")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener servicio: {e}")

@servicioRouter.post("/", status_code=status.HTTP_201_CREATED)
async def crear_servicio(servicio: ServicioBase):
    try:
        insert_query = """
        INSERT INTO servicios (Nombre, Descripcion, Precio)
        VALUES (%s, %s, %s)
        """
        values = (servicio.nombre, servicio.descripcion, servicio.precio)
        cleverCursor.execute(insert_query, values)
        mysqlConn.commit()
        return {"message": "Servicio creado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al crear servicio: {e}")

@servicioRouter.put("/{servicio_id}", status_code=status.HTTP_200_OK)
async def actualizar_servicio(servicio_id: int, servicio: ServicioBase):
    try:
        update_query = """
        UPDATE servicios 
        SET Nombre = %s, Descripcion = %s, Precio = %s
        WHERE Id_Servicio = %s
        """
        values = (servicio.nombre, servicio.descripcion, servicio.precio, servicio_id)
        cleverCursor.execute(update_query, values)
        mysqlConn.commit()
        return {"message": "Servicio actualizado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al actualizar servicio: {e}")

@servicioRouter.delete("/{servicio_id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_servicio(servicio_id: int):
    try:
        cleverCursor.execute('DELETE FROM servicios WHERE Id_Servicio = %s', (servicio_id,))
        mysqlConn.commit()
        return {"message": "Servicio eliminado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al eliminar servicio: {e}")
