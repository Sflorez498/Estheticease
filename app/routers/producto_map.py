from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field
from database.Clever_MySQL_conn import cleverCursor, mysqlConn  # Asegúrate de que esta importación sea correcta

# Definición del router
productoRouter = APIRouter()

# Modelo de datos para el producto
class ProductoDB(BaseModel):
    id_producto: int
    nombre_producto: str
    categoria: str
    precio: int = Field(gt=0)
    stock: int = Field(ge=0)

# Ruta para obtener todos los productos
@productoRouter.get("/productos/", status_code=status.HTTP_200_OK)
async def obtener_productos():
    try:
        cleverCursor.execute('SELECT * FROM producto')
        result = cleverCursor.fetchall()
        return result
    except Exception as err:
        raise HTTPException(status_code=500, detail=f"Error inesperado: {err}")

# Ruta para obtener un producto por ID
@productoRouter.get("/productos/{id_producto}", status_code=status.HTTP_200_OK)
def obtener_producto_por_id(id_producto: int):
    try:
        cleverCursor.execute("SELECT * FROM producto WHERE id_producto = %s", (id_producto,))
        result = cleverCursor.fetchone()
        if result:
            return result
        else:
            raise HTTPException(status_code=404, detail="Producto no encontrado")
    except Exception as err:
        raise HTTPException(status_code=500, detail=f"Error inesperado: {err}")

# Ruta para crear un nuevo producto
@productoRouter.post("/productos/", status_code=status.HTTP_201_CREATED)
def crear_producto(producto: ProductoDB):
    try:
        cleverCursor.execute("SELECT * FROM producto WHERE id_producto = %s", (producto.id_producto,))
        if cleverCursor.fetchone():
            raise HTTPException(status_code=409, detail="Ya existe un producto con ese ID")
        
        insert_query = """
        INSERT INTO producto (id_producto, nombre_producto, categoria, precio, stock)
        VALUES (%s, %s, %s, %s, %s)
        """
        values = (
            producto.id_producto,
            producto.nombre_producto,
            producto.categoria,
            producto.precio,
            producto.stock,
        )
        cleverCursor.execute(insert_query, values)
        mysqlConn.commit()
        return {"message": "Producto creado exitosamente"}
    except Exception as err:
        raise HTTPException(status_code=400, detail=f"Error inesperado al crear el producto: {err}")
