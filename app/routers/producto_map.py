from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from app.database.Clever_MySQL_conn import cleverCursor, mysqlConn
from typing import List, Optional
from decimal import Decimal

class ProductoBase(BaseModel):
    nombre: str
    descripcion: str
    precio: Decimal
    stock: int
    imagen_url: str
    categoria: str

class Producto(ProductoBase):
    id_producto: Optional[int] = None

productoRouter = APIRouter()

@productoRouter.get("/", status_code=status.HTTP_200_OK)
async def listar_productos():
    try:
        cleverCursor.execute('''
            SELECT id_producto, nombre_producto, categoria, inventario as stock, precio, is_active 
            FROM Productos 
            WHERE inventario > 0 
            ORDER BY categoria, nombre_producto
        ''')
        productos = cleverCursor.fetchall()
        return productos
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener productos: {e}")

@productoRouter.get("/categoria/{categoria}", status_code=status.HTTP_200_OK)
async def productos_por_categoria(categoria: str):
    try:
        cleverCursor.execute('''
            SELECT id_producto, nombre_producto, categoria, inventario as stock, precio, is_active 
            FROM Productos 
            WHERE categoria = %s AND inventario > 0
        ''', (categoria,))
        productos = cleverCursor.fetchall()
        
        # Formatear los productos para que coincidan con el modelo
        productos_formateados = []
        for producto in productos:
            try:
                productos_formateados.append({
                    'id_producto': producto[0],
                    'nombre': producto[1],
                    'descripcion': producto[2],
                    'precio': float(producto[3]),  # Convertir a float para JSON
                    'stock': producto[4],
                    'imagen': producto[5],
                    'categoria': producto[6]
                })
            except Exception as e:
                print(f"Error formateando producto: {e}")
                continue
        
        return productos_formateados
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener productos: {e}")

@productoRouter.post("/", status_code=status.HTTP_201_CREATED)
async def crear_producto(producto: ProductoBase):
    try:
        insert_query = """
        INSERT INTO productos (Nombre, Descripcion, Precio, Stock, Imagen_URL, Categoria)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        values = (
            producto.nombre,
            producto.descripcion,
            float(producto.precio),
            producto.stock,
            producto.imagen_url,
            producto.categoria
        )
        cleverCursor.execute(insert_query, values)
        mysqlConn.commit()
        return {"message": "Producto creado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al crear producto: {e}")

@productoRouter.put("/stock/{producto_id}", status_code=status.HTTP_200_OK)
async def actualizar_stock(producto_id: int, cantidad: int):
    try:
        # Verificar stock actual
        cleverCursor.execute(
            "SELECT Stock FROM productos WHERE Id_Producto = %s",
            (producto_id,)
        )
        stock_actual = cleverCursor.fetchone()
        if not stock_actual or stock_actual['Stock'] < cantidad:
            raise HTTPException(status_code=400, detail="Stock insuficiente")

        # Actualizar stock
        nuevo_stock = stock_actual['Stock'] - cantidad
        cleverCursor.execute(
            "UPDATE productos SET Stock = %s WHERE Id_Producto = %s",
            (nuevo_stock, producto_id)
        )
        mysqlConn.commit()
        return {"message": "Stock actualizado exitosamente"}
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al actualizar stock: {e}")
