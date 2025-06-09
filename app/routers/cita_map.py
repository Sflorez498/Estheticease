from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from database.Clever_MySQL_conn import cleverCursor, mysqlConn
from datetime import datetime
from typing import List, Optional

citaRouter = APIRouter()

class CitaBase(BaseModel):
    id_clientes: int
    id_servicio: int
    fecha_cita: str  # Formato ISO: "YYYY-MM-DD"
    estado: str

class CitaDB(CitaBase):
    id_cita: Optional[int] = None

@citaRouter.get("/", status_code=status.HTTP_200_OK)
async def obtener_citas():
    try:
        cleverCursor.execute('''
            SELECT c.*, s.Nombre as servicio_nombre, cl.Nombre as cliente_nombre 
            FROM citas c 
            JOIN servicios s ON c.Id_Servicio = s.Id_Servicio
            JOIN clientes cl ON c.Id_Clientes = cl.Id_Cliente
        ''')
        result = cleverCursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener citas: {e}")

@citaRouter.get("/cliente/{id_cliente}", status_code=status.HTTP_200_OK)
async def obtener_citas_cliente(id_cliente: int):
    try:
        cleverCursor.execute('''
            SELECT c.*, s.Nombre as servicio_nombre 
            FROM citas c 
            JOIN servicios s ON c.Id_Servicio = s.Id_Servicio
            WHERE c.Id_Clientes = %s
        ''', (id_cliente,))
        result = cleverCursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener citas del cliente: {e}")

@citaRouter.get("/{id_cita}", status_code=status.HTTP_200_OK)
def obtener_cita_por_id(id_cita: int):
    try:
        select_query = '''
            SELECT c.*, s.Nombre as servicio_nombre, cl.Nombre as cliente_nombre 
            FROM citas c 
            JOIN servicios s ON c.Id_Servicio = s.Id_Servicio
            JOIN clientes cl ON c.Id_Clientes = cl.Id_Cliente
            WHERE c.Id_Cita = %s
        '''
        cleverCursor.execute(select_query, (id_cita,))
        result = cleverCursor.fetchone()
        if result:
            return result
        else:
            raise HTTPException(status_code=404, detail="Cita no encontrada")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al buscar cita: {e}")

@citaRouter.post("/", status_code=status.HTTP_201_CREATED)
def crear_cita(cita: CitaBase):
    try:
        # Verificar disponibilidad
        cleverCursor.execute(
            "SELECT COUNT(*) FROM citas WHERE Fecha_Cita = %s",
            (cita.fecha_cita,)
        )
        count = cleverCursor.fetchone()[0]
        if count >= 8:  # Máximo 8 citas por día
            raise HTTPException(status_code=400, detail="No hay disponibilidad para esta fecha")

        insert_query = """
        INSERT INTO citas (Id_Clientes, Id_Servicio, Fecha_Cita, Estado)
        VALUES (%s, %s, %s, %s)
        """
        values = (
            cita.id_clientes,
            cita.id_servicio,
            cita.fecha_cita,
            cita.estado
        )
        cleverCursor.execute(insert_query, values)
        mysqlConn.commit()
        return {"message": "Cita creada exitosamente"}
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al crear la cita: {e}")

@citaRouter.delete("/{id_cita}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_cita(id_cita: int):
    try:
        # Verificar si la cita existe
        cleverCursor.execute("SELECT * FROM citas WHERE Id_Cita = %s", (id_cita,))
        if not cleverCursor.fetchone():
            raise HTTPException(status_code=404, detail="Cita no encontrada")

        # Eliminar la cita
        cleverCursor.execute("DELETE FROM citas WHERE Id_Cita = %s", (id_cita,))
        mysqlConn.commit()
        return {"message": "Cita eliminada exitosamente"}
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al eliminar la cita: {e}")

@citaRouter.put("/{id_cita}", status_code=status.HTTP_200_OK)
def actualizar_estado_cita(id_cita: int, estado: str):
    try:
        cleverCursor.execute(
            "UPDATE citas SET Estado = %s WHERE Id_Cita = %s",
            (estado, id_cita)
        )
        mysqlConn.commit()
        return {"message": "Estado de la cita actualizado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al actualizar el estado de la cita: {e}")
