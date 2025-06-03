from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from database.Clever_MySQL_conn import cleverCursor, mysqlConn

citaRouter = APIRouter()

class CitaDB(BaseModel):
    id_cita: int  # Cambiado a snake_case
    id_clientes: int  # Cambiado a snake_case
    id_servicio: int  # Cambiado a snake_case
    fecha_cita: str  # Formato ISO: "YYYY-MM-DD"
    estado: str

@citaRouter.get("/citas/", status_code=status.HTTP_200_OK)
async def obtener_citas():
    try:
        cleverCursor.execute('SELECT * FROM citas')
        result = cleverCursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener citas: {e}")

@citaRouter.get("/citas/{id_cita}", status_code=status.HTTP_200_OK)
def obtener_cita_por_id(id_cita: int):
    try:
        select_query = "SELECT * FROM citas WHERE Id_Cita = %s"
        cleverCursor.execute(select_query, (id_cita,))
        result = cleverCursor.fetchone()
        if result:
            return result
        else:
            raise HTTPException(status_code=404, detail="Cita no encontrada")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al buscar cita: {e}")

@citaRouter.post("/citas/", status_code=status.HTTP_201_CREATED)
def crear_cita(cita: CitaDB):
    try:
        insert_query = """
        INSERT INTO citas (Id_Cita, Id_Clientes, Id_Servicio, Fecha_Cita, Estado)
        VALUES (%s, %s, %s, %s, %s)
        """
        values = (
            cita.id_cita,
            cita.id_clientes,
            cita.id_servicio,
            cita.fecha_cita,
            cita.estado
        )
        cleverCursor.execute(insert_query, values)
        mysqlConn.commit()
        return {"message": "Cita creada exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al crear la cita: {e}")

# Nueva ruta para eliminar una cita
@citaRouter.delete("/citas/{id_cita}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_cita(id_cita: int):
    try:
        # Verificar si la cita existe antes de intentar eliminarla
        select_query = "SELECT * FROM citas WHERE Id_Cita = %s"
        cleverCursor.execute(select_query, (id_cita,))
        result = cleverCursor.fetchone()
        if not result:
            raise HTTPException(status_code=404, detail="Cita no encontrada")

        # Eliminar la cita
        delete_query = "DELETE FROM citas WHERE Id_Cita = %s"
        cleverCursor.execute(delete_query, (id_cita,))
        mysqlConn.commit()
        return {"message": "Cita eliminada exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al eliminar la cita: {e}")
