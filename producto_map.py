from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from Clever_MySQL_conn import cleverCursor, mysqlConn

ProductoRouter =  APIRouter()

class productoDB(BaseModel):
    id_producto : int
    nombre_producto : str
    categoria : str 
    precio : int
    stock : int
    
@ProductoRouter.get("/SPA_Producto/", status_code=status.HTTP_302_FOUND)
async def get_users():
    selectAll_query = 'Select * from Servicios'
    cleverCursor.execute(selectAll_query)
    result = cleverCursor.fetchall()
    return result


@ProductoRouter.get("/SPA_Producto/{id_producto}", status_code=status.HTTP_200_OK)
def get_user_by_id(id_producto: int):
    select_query = "SELECT * FROM producto WHERE id_producto = %s"
    cleverCursor.execute(select_query, (id_producto,))
    result = cleverCursor.fetchone()
    if result:
        return result
    else:
        raise HTTPException(status_code=404, detail="producto no encontrado")
    
@ProductoRouter.post("/spa_crea_producto/", status_code=status.HTTP_201_CREATED)
def insert_user(ProductoPost: productoDB):
    insert_query = """
    INSERT INTO producto (Id_Servicio, nombre_servicio, descripcion, precio)
    VALUES (%s, %s, %s, %s, %s)
    """
    values = (ProductoPost.id_producto, ProductoPost.nombre_producto, ProductoPost.categoria, ProductoPost.precio, ProductoPost.stock)

    try:
        cleverCursor.execute(insert_query, values)
        mysqlConn.commit()
    except mysqlConn.connector.Error as err:
       raise HTTPException(status_code=400, detail=f"Error: {err}")

    return {"message": "User inserted successfully"}