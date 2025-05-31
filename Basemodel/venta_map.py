from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from Clever_MySQL_conn import cleverCursor, mysqlConn

VentaRouter =  APIRouter()

class ventaDB(BaseModel):
    Id_ventas : int
    Id_Clientes: int
    Id_Producto : int 
    Cantidad : int
    Total : int
    Fecha_ventas : int
    
    
@VentaRouter.get("/SPA_Venta/", status_code=status.HTTP_302_FOUND)
async def get_users():
    selectAll_query = 'Select * from Servicios'
    cleverCursor.execute(selectAll_query)
    result = cleverCursor.fetchall()
    return result


@VentaRouter.get("/SPA_Venta/{Id_ventas}", status_code=status.HTTP_200_OK)
def get_user_by_id(Id_ventas: int):
    select_query = "SELECT * FROM servicio WHERE Id_ventas = %s"
    cleverCursor.execute(select_query, (Id_ventas,))
    result = cleverCursor.fetchone()
    if result:
        return result
    else:
        raise HTTPException(status_code=404, detail="venta no encontrada")
    
@VentaRouter.post("/spa_crea_venta/", status_code=status.HTTP_201_CREATED)
def insert_user(ventaPost: ventaDB):
    insert_query = """
    INSERT INTO servicio (Id_ventas, Id_Clientes, Id_Producto, Cantidad, Total, Fecha_ventas)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    values = (ventaPost.Id_ventas, ventaPost.Id_Clientes, ventaPost.Cantidad, ventaPost.Total, ventaPost.Fecha_ventas)

    try:
        cleverCursor.execute(insert_query, values)
        mysqlConn.commit()
    except mysqlConn.connector.Error as err:
       raise HTTPException(status_code=400, detail=f"Error: {err}")

    return {"message": "User inserted successfully"}