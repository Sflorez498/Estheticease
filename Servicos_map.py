from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from Clever_MySQL_conn import cleverCursor, mysqlConn

servicoRouter =  APIRouter()

class servicosDB(BaseModel):
    Id_Servicio : int
    nombre_servicio : str
    descripcion : str 
    precio : int
    
@servicoRouter.get("/SPA_SERVICIO/", status_code=status.HTTP_302_FOUND)
async def get_users():
    selectAll_query = 'Select * from Servicios'
    cleverCursor.execute(selectAll_query)
    result = cleverCursor.fetchall()
    return result


@servicoRouter.get("/SPA_SERVICIO/{Id_servicio}", status_code=status.HTTP_200_OK)
def get_user_by_id(Id_servicio: int):
    select_query = "SELECT * FROM servicio WHERE Id_Servicio = %s"
    cleverCursor.execute(select_query, (Id_servicio,))
    result = cleverCursor.fetchone()
    if result:
        return result
    else:
        raise HTTPException(status_code=404, detail="Servicios no encontrado")
    
@servicoRouter.post("/spa_crea_servico/", status_code=status.HTTP_201_CREATED)
def insert_user(servicioPost: servicosDB):
    insert_query = """
    INSERT INTO servicio (Id_Servicio, nombre_servicio, descripcion, precio)
    VALUES (%s, %s, %s, %s)
    """
    values = (servicioPost.Id_Servicio, servicioPost.nombre_servicio, servicioPost.descripcion, servicioPost.precio)

    try:
        cleverCursor.execute(insert_query, values)
        mysqlConn.commit()
    except mysqlConn.connector.Error as err:
       raise HTTPException(status_code=400, detail=f"Error: {err}")

    return {"message": "User inserted successfully"}