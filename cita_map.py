from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from Clever_MySQL_conn import cleverCursor, mysqlConn

citaRouter =  APIRouter()

class citaDB(BaseModel):
    Id_Cita : int
    Id_Clientes: int
    Id_Servicio : int 
    Fecha_Cita : int
    Estado : str
    
    
    
@citaRouter.get("/Citas/", status_code=status.HTTP_302_FOUND)
async def get_users():
    selectAll_query = 'Select * from Servicios'
    cleverCursor.execute(selectAll_query)
    result = cleverCursor.fetchall()
    return result


@citaRouter.get("/citas/{Id_ventas}", status_code=status.HTTP_200_OK)
def get_user_by_id(Id_Cita: int):
    select_query = "SELECT * FROM servicio WHERE Id_Cita = %s"
    cleverCursor.execute(select_query, (Id_Cita,))
    result = cleverCursor.fetchone()
    if result:
        return result
    else:
        raise HTTPException(status_code=404, detail="cita no encontrada")
    
@citaRouter.post("/spa_crea_cita/", status_code=status.HTTP_201_CREATED)
def insert_user(citaPost: citaDB):
    insert_query = """
    INSERT INTO citas (Id_ventas, Id_Clientes, Id_Producto, Cantidad, Total)
    VALUES (%s, %s, %s, %s, %s)
    """
    values = (citaPost.Id_ventas, citaPost.Id_Clientes, citaPost.Cantidad, citaPost.Total)

    try:
        cleverCursor.execute(insert_query, values)
        mysqlConn.commit()
    except mysqlConn.connector.Error as err:
       raise HTTPException(status_code=400, detail=f"Error: {err}")

    return {"message": "User inserted successfully"}
