from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from app.database.Clever_MySQL_conn import cleverCursor, mysqlConn  # Asegúrate de que esta importación sea correcta

# Definición del router
ventaRouter = APIRouter()

# Modelo de datos para la venta
class VentaDB(BaseModel):
    id_ventas: int  # Cambiado a snake_case
    id_clientes: int  # Cambiado a snake_case
    id_producto: int  # Cambiado a snake_case
    cantidad: int
    total: float  # Cambiado a float para manejar decimales
    fecha_ventas: str  # Formato "YYYY-MM-DD"

# Ruta para obtener todas las ventas
@ventaRouter.get("/ventas/", status_code=status.HTTP_200_OK)
async def obtener_ventas():
    try:
        cleverCursor.execute('SELECT * FROM ventas')
        result = cleverCursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener ventas: {e}")

# Ruta para obtener una venta por ID
@ventaRouter.get("/ventas/{id_ventas}", status_code=status.HTTP_200_OK)
def obtener_venta_por_id(id_ventas: int):
    try:
        select_query = "SELECT * FROM ventas WHERE Id_ventas = %s"
        cleverCursor.execute(select_query, (id_ventas,))
        result = cleverCursor.fetchone()
        if result:
            return result
        else:
            raise HTTPException(status_code=404, detail="Venta no encontrada")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al buscar venta: {e}")

# Ruta para crear una nueva venta
@ventaRouter.post("/ventas/", status_code=status.HTTP_201_CREATED)
def crear_venta(venta: VentaDB):
    try:
        insert_query = """
        INSERT INTO ventas (Id_ventas, Id_Clientes, Id_Producto, Cantidad, Total, Fecha_ventas)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        values = (
            venta.id_ventas,
            venta.id_clientes,
            venta.id_producto,
            venta.cantidad,
            venta.total,
            venta.fecha_ventas
        )
        cleverCursor.execute(insert_query, values)
        mysqlConn.commit()
        return {"message": "Venta creada exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al crear la venta: {e}")
