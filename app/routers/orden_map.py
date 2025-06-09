from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from database.Clever_MySQL_conn import cleverCursor, mysqlConn
from typing import List, Optional
from datetime import datetime

class ProductoOrden(BaseModel):
    id_producto: int
    cantidad: int
    precio_unitario: float

class OrdenBase(BaseModel):
    id_cliente: int
    productos: List[ProductoOrden]
    total: float
    estado: str

class Orden(OrdenBase):
    id_orden: Optional[int] = None
    fecha: Optional[datetime] = None

ordenRouter = APIRouter()

@ordenRouter.post("/", status_code=status.HTTP_201_CREATED)
async def crear_orden(orden: OrdenBase):
    try:
        # Iniciar transacción
        mysqlConn.begin()
        
        # Insertar orden principal
        insert_orden = """
        INSERT INTO ordenes (Id_Cliente, Total, Estado, Fecha)
        VALUES (%s, %s, %s, NOW())
        """
        cleverCursor.execute(insert_orden, (
            orden.id_cliente,
            orden.total,
            orden.estado
        ))
        
        id_orden = cleverCursor.lastrowid
        
        # Insertar detalles de la orden
        insert_detalle = """
        INSERT INTO orden_detalles (Id_Orden, Id_Producto, Cantidad, Precio_Unitario)
        VALUES (%s, %s, %s, %s)
        """
        for producto in orden.productos:
            cleverCursor.execute(insert_detalle, (
                id_orden,
                producto.id_producto,
                producto.cantidad,
                producto.precio_unitario
            ))
            
            # Actualizar stock
            cleverCursor.execute(
                "UPDATE productos SET Stock = Stock - %s WHERE Id_Producto = %s",
                (producto.cantidad, producto.id_producto)
            )
        
        mysqlConn.commit()
        return {"message": "Orden creada exitosamente", "id_orden": id_orden}
    
    except Exception as e:
        mysqlConn.rollback()
        raise HTTPException(status_code=400, detail=f"Error al crear la orden: {e}")

@ordenRouter.get("/cliente/{id_cliente}", status_code=status.HTTP_200_OK)
async def obtener_ordenes_cliente(id_cliente: int):
    try:
        query = """
        SELECT o.*, 
               od.Id_Producto, od.Cantidad, od.Precio_Unitario,
               p.Nombre as Nombre_Producto
        FROM ordenes o
        JOIN orden_detalles od ON o.Id_Orden = od.Id_Orden
        JOIN productos p ON od.Id_Producto = p.Id_Producto
        WHERE o.Id_Cliente = %s
        ORDER BY o.Fecha DESC
        """
        cleverCursor.execute(query, (id_cliente,))
        ordenes = cleverCursor.fetchall()
        
        # Organizar los resultados por orden
        ordenes_organizadas = {}
        for orden in ordenes:
            id_orden = orden['Id_Orden']
            if id_orden not in ordenes_organizadas:
                ordenes_organizadas[id_orden] = {
                    'id_orden': id_orden,
                    'fecha': orden['Fecha'],
                    'total': orden['Total'],
                    'estado': orden['Estado'],
                    'productos': []
                }
            
            ordenes_organizadas[id_orden]['productos'].append({
                'id_producto': orden['Id_Producto'],
                'nombre': orden['Nombre_Producto'],
                'cantidad': orden['Cantidad'],
                'precio_unitario': orden['Precio_Unitario']
            })
        
        return list(ordenes_organizadas.values())
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener las órdenes: {e}")

@ordenRouter.get("/{id_orden}", status_code=status.HTTP_200_OK)
async def obtener_orden(id_orden: int):
    try:
        query = """
        SELECT o.*, 
               od.Id_Producto, od.Cantidad, od.Precio_Unitario,
               p.Nombre as Nombre_Producto
        FROM ordenes o
        JOIN orden_detalles od ON o.Id_Orden = od.Id_Orden
        JOIN productos p ON od.Id_Producto = p.Id_Producto
        WHERE o.Id_Orden = %s
        """
        cleverCursor.execute(query, (id_orden,))
        detalles = cleverCursor.fetchall()
        
        if not detalles:
            raise HTTPException(status_code=404, detail="Orden no encontrada")
        
        orden = {
            'id_orden': detalles[0]['Id_Orden'],
            'fecha': detalles[0]['Fecha'],
            'total': detalles[0]['Total'],
            'estado': detalles[0]['Estado'],
            'productos': []
        }
        
        for detalle in detalles:
            orden['productos'].append({
                'id_producto': detalle['Id_Producto'],
                'nombre': detalle['Nombre_Producto'],
                'cantidad': detalle['Cantidad'],
                'precio_unitario': detalle['Precio_Unitario']
            })
        
        return orden
    
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener la orden: {e}")

@ordenRouter.put("/{id_orden}/estado", status_code=status.HTTP_200_OK)
async def actualizar_estado_orden(id_orden: int, estado: str):
    try:
        cleverCursor.execute(
            "UPDATE ordenes SET Estado = %s WHERE Id_Orden = %s",
            (estado, id_orden)
        )
        mysqlConn.commit()
        return {"message": "Estado de la orden actualizado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al actualizar el estado: {e}") 