# Rutas y modelos relacionados con citas y disponibilidad

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from app.database.Clever_MySQL_conn import cleverCursor, mysqlConn
from datetime import datetime, timedelta
from typing import List, Optional
import bcrypt

citaRouter = APIRouter()

# Modelos de datos para servicios, empleados y citas

class Servicio(BaseModel):
    """Modelo para representar un servicio del salón"""
    id_servicio: int
    nombre: str
    duracion: int  # En minutos
    precio: float

class Empleado(BaseModel):
    """Modelo para representar un empleado del salón"""
    id_empleado: int
    nombre: str
    especialidad: str

class Disponibilidad(BaseModel):
    """Modelo para representar la disponibilidad de un empleado"""
    id_disponibilidad: int
    id_empleado: int
    fecha: str  # Formato YYYY-MM-DD
    hora: str   # Formato HH:MM
    estado: bool  # True si está disponible, False si no

class CitaBase(BaseModel):
    """Modelo base para crear una cita"""
    id_cliente: int
    id_empleado: int
    id_servicio: int
    fecha: str  # Formato YYYY-MM-DD
    hora: str   # Formato HH:MM
    estado: str = "Pendiente"  # Pendiente por defecto
    notas: Optional[str] = None  # Notas opcionales sobre la cita

class CitaDB(CitaBase):
    """Modelo completo que incluye el ID de la cita"""
    id_cita: Optional[int] = None

@citaRouter.get("/", status_code=status.HTTP_200_OK)
async def obtener_citas():
    try:
        cleverCursor.execute('''
            SELECT c.id_cita, c.id_cliente, c.id_servicio, c.id_empleado, c.fecha, c.hora, 
                   c.estado, c.notas, s.nombre_servicio as servicio_nombre, 
                   cl.nombre as cliente_nombre 
            FROM citas c 
            JOIN servicios s ON c.id_servicio = s.id_servicio
            JOIN clientes cl ON c.id_cliente = cl.id_cliente
        ''')
        result = cleverCursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener citas: {e}")

@citaRouter.get("/cliente/{id_cliente}", status_code=status.HTTP_200_OK)
async def obtener_citas_cliente(id_cliente: int):
    try:
        cleverCursor.execute('''
            SELECT c.id_cita, c.id_cliente, c.id_servicio, c.id_empleado, c.fecha, c.hora, 
                   c.estado, c.notas, s.nombre_servicio as servicio_nombre 
            FROM citas c 
            JOIN servicios s ON c.id_servicio = s.id_servicio
            WHERE c.id_cliente = %s
        ''', (id_cliente,))
        citas = cleverCursor.fetchall()
        
        # Convertir los resultados a un formato más amigable
        citas_formateadas = []
        for cita in citas:
            citas_formateadas.append({
                'id_cita': cita[0],
                'id_cliente': cita[1],
                'id_servicio': cita[2],
                'id_empleado': cita[3],
                'fecha': cita[4],
                'hora': cita[5],
                'estado': cita[6],
                'notas': cita[7],
                'nombre_servicio': cita[8]
            })
        return citas_formateadas
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener citas del cliente: {e}")

@citaRouter.get("/{id_cita}", status_code=status.HTTP_200_OK)
def obtener_cita_por_id(id_cita: int):
    try:
        select_query = '''
            SELECT c.id_cita, c.id_cliente, c.id_servicio, c.id_empleado, c.fecha, c.hora, 
                   c.estado, c.notas, s.nombre_servicio as servicio_nombre, 
                   cl.nombre as cliente_nombre 
            FROM citas c 
            JOIN servicios s ON c.id_servicio = s.id_servicio
            JOIN clientes cl ON c.id_cliente = cl.id_cliente
            WHERE c.id_cita = %s
        '''
        cleverCursor.execute(select_query, (id_cita,))
        result = cleverCursor.fetchone()
        if result:
            return result
        else:
            raise HTTPException(status_code=404, detail="Cita no encontrada")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al buscar cita: {e}")

@citaRouter.get("/disponibilidad", status_code=status.HTTP_200_OK)
def obtener_disponibilidad(fecha: str):
    """
    Obtiene la disponibilidad de empleados para una fecha específica
    """
    try:
        # Asegurar que la fecha esté en el formato correcto YYYY-MM-DD
        try:
            fecha_formateada = datetime.strptime(fecha, '%Y-%m-%d').strftime('%Y-%m-%d')
        except ValueError:
            raise HTTPException(status_code=400, detail="Formato de fecha inválido. Use YYYY-MM-DD")
        
        cleverCursor.execute('''
            SELECT d.id_disponibilidad, d.id_empleado, d.fecha, d.hora, 
                   d.estado as estado_disponibilidad, e.nombre as empleado_nombre, 
                   e.especialidad
            FROM disponibilidad d
            JOIN empleados e ON d.id_empleado = e.id_empleado
            WHERE d.fecha = %s AND d.estado = 1
        ''', (fecha_formateada,))
        disponibilidad = cleverCursor.fetchall()
        
        # Convertir los resultados a un formato más amigable
        disponibilidad_formateada = []
        for disp in disponibilidad:
            disponibilidad_formateada.append({
                'id_disponibilidad': disp[0],
                'id_empleado': disp[1],
                'fecha': disp[2],
                'hora': disp[3],
                'estado': disp[4],
                'empleado_nombre': disp[5],
                'especialidad': disp[6]
            })
        return disponibilidad_formateada
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener disponibilidad: {e}")

# Redirigir a la ruta correcta de servicios
@citaRouter.get("/servicios", status_code=status.HTTP_200_OK)
def obtener_servicios():
    try:
        cleverCursor.execute('SELECT id_servicio, nombre_servicio, duracion, precio FROM servicios')
        servicios = cleverCursor.fetchall()
        return servicios
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener servicios: {e}")
    """
    Obtiene la lista de servicios disponibles
    """
    try:
        cleverCursor.execute('''
            SELECT id_servicio, nombre_servicio as nombre, duracion_minutos as duracion, 
                   precio, is_active as estado 
            FROM servicios 
            WHERE is_active = 1
        ''')
        servicios = cleverCursor.fetchall()
        return servicios
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener servicios: {e}")

# Redirigir a la ruta correcta de empleados
@citaRouter.get("/empleados", status_code=status.HTTP_200_OK)
def obtener_empleados():
    try:
        cleverCursor.execute('''
            SELECT id_empleado, nombre, especialidad 
            FROM empleados 
            WHERE is_active = 1
        ''')
        empleados = cleverCursor.fetchall()
        return empleados
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener empleados: {e}")
    """
    Obtiene la lista de empleados disponibles
    """
    try:
        cleverCursor.execute('''
            SELECT id_empleado, nombre, especialidad 
            FROM empleados 
            WHERE is_active = 1
        ''')
        empleados = cleverCursor.fetchall()
        # Convertir los resultados a un formato más amigable
        empleados_formateados = []
        for empleado in empleados:
            empleados_formateados.append({
                'id_empleado': empleado[0],
                'nombre': empleado[1],
                'especialidad': empleado[2]
            })
        return empleados_formateados
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener empleados: {e}")
    finally:
        mysqlConn.commit()

@citaRouter.post("/", status_code=status.HTTP_201_CREATED)
def crear_cita(cita: CitaBase):
    """
    Crea una nueva cita
    """
    try:
        # Verificar disponibilidad
        cleverCursor.execute('''
            SELECT COUNT(*) FROM citas 
            WHERE fecha = %s AND hora = %s AND id_empleado = %s
        ''', (cita.fecha, cita.hora, cita.id_empleado))
        count = cleverCursor.fetchone()[0]
        if count > 0:
            raise HTTPException(status_code=400, detail="El profesional ya tiene una cita en ese horario")

        # Verificar si el horario está disponible
        cleverCursor.execute('''
            SELECT COUNT(*) FROM disponibilidad 
            WHERE fecha = %s AND hora = %s AND id_empleado = %s AND estado = 1
        ''', (cita.fecha, cita.hora, cita.id_empleado))
        disponible = cleverCursor.fetchone()[0]
        if disponible == 0:
            raise HTTPException(status_code=400, detail="El horario no está disponible")

        # Insertar la cita
        insert_query = """
        INSERT INTO citas (id_cliente, id_empleado, id_servicio, fecha, hora, estado, notas)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        values = (
            cita.id_cliente,
            cita.id_empleado,
            cita.id_servicio,
            cita.fecha,
            cita.hora,
            cita.estado,
            cita.notas
        )
        cleverCursor.execute(insert_query, values)
        mysqlConn.commit()

        # Actualizar la disponibilidad
        cleverCursor.execute('''
            UPDATE disponibilidad 
            SET estado = 0 
            WHERE fecha = %s AND hora = %s AND id_empleado = %s
        ''', (cita.fecha, cita.hora, cita.id_empleado))
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
