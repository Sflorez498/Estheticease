from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from app.database.Clever_MySQL_conn import cleverCursor, mysqlConn
from datetime import datetime
from typing import List, Optional

citaRouter = APIRouter()

# ----------- Modelos ----------- #

class Servicio(BaseModel):
    id_servicio: int
    nombre: str
    duracion: int
    precio: float

class Empleado(BaseModel):
    id_empleado: int
    nombre: str
    especialidad: str

class Disponibilidad(BaseModel):
    id_disponibilidad: int
    id_empleado: int
    fecha: str
    hora: str
    estado: bool

class CitaBase(BaseModel):
    id_cliente: int
    id_empleado: int
    id_servicio: int
    fecha: str
    hora: str
    estado: str = "Pendiente"
    notas: Optional[str] = None

class CitaDB(CitaBase):
    id_cita: Optional[int] = None

# ----------- Endpoints ----------- #

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
        return cleverCursor.fetchall()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener citas: {e}")

@citaRouter.get("/cliente/{id_cliente}", status_code=status.HTTP_200_OK)
async def obtener_citas_cliente(id_cliente: int):
    """
    Obtiene todas las citas de un cliente específico
    """
    if id_cliente <= 0:
        raise HTTPException(status_code=400, detail="ID de cliente inválido")
    try:
        print(f"Consultando citas para cliente ID: {id_cliente}")
        cleverCursor.execute('''
            SELECT c.id_cita, c.id_cliente, c.id_servicio, c.id_empleado, 
                   c.fecha as fecha_completa, c.estado, c.notas,
                   s.nombre as nombre_servicio,
                   e.nombre as nombre_empleado, e.especialidad
            FROM citas c 
            JOIN servicios s ON c.id_servicio = s.id_servicio
            JOIN empleados e ON c.id_empleado = e.id_empleado
            WHERE c.id_cliente = %s AND c.estado != 'Cancelada'
            ORDER BY c.fecha
        ''', (id_cliente,))
        citas = cleverCursor.fetchall()
        print(f"Encontradas {len(citas)} citas para el cliente")
        if not citas:
            return []  # Retornar lista vacía en lugar de error 404
        
        # Formatear los resultados
        citas_formateadas = []
        for cita in citas:
            try:
                fecha_completa = cita[4]
                cita_formateada = {
                    'id_cita': cita[0],
                    'id_cliente': cita[1],
                    'id_servicio': cita[2],
                    'id_empleado': cita[3],
                    'fecha': fecha_completa.strftime('%Y-%m-%d'),
                    'hora': fecha_completa.strftime('%H:%M'),
                    'estado': cita[5],
                    'notas': cita[6],
                    'nombre_servicio': cita[7],
                    'nombre_empleado': cita[8],
                    'especialidad': cita[9]
                }
                citas_formateadas.append(cita_formateada)
            except Exception as e:
                print(f"Error formateando cita {cita[0]}: {str(e)}")
                continue
        return citas_formateadas
    except mysql.connector.Error as sql_err:
        print(f"Error MySQL: {sql_err}")
        raise HTTPException(status_code=500, detail=f"Error MySQL: {sql_err}")
    except Exception as e:
        print(f"Error inesperado: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")

@citaRouter.get("/{id_cita}", status_code=status.HTTP_200_OK)
async def obtener_cita_por_id(id_cita: int):
    """
    Obtiene los detalles de una cita específica
    """
    if id_cita <= 0:
        raise HTTPException(status_code=400, detail="ID inválido")
    try:
        cleverCursor.execute('''
            SELECT c.id_cita, c.id_cliente, c.id_servicio, c.id_empleado, 
                   c.fecha as fecha_completa, c.estado, c.notas,
                   s.nombre as nombre_servicio, s.duracion,
                   e.nombre as nombre_empleado, e.especialidad,
                   cl.nombre as nombre_cliente
            FROM citas c 
            JOIN servicios s ON c.id_servicio = s.id_servicio
            JOIN empleados e ON c.id_empleado = e.id_empleado
            JOIN clientes cl ON c.id_cliente = cl.id_cliente
            WHERE c.id_cita = %s
        ''', (id_cita,))
        r = cleverCursor.fetchone()
        if not r:
            raise HTTPException(status_code=404, detail="Cita no encontrada")
        
        fecha_completa = r[4]
        return {
            'id_cita': r[0],
            'id_cliente': r[1],
            'id_servicio': r[2],
            'id_empleado': r[3],
            'fecha': fecha_completa.strftime('%Y-%m-%d'),
            'hora': fecha_completa.strftime('%H:%M'),
            'estado': r[5],
            'notas': r[6],
            'nombre_servicio': r[7],
            'duracion': r[8],
            'nombre_empleado': r[9],
            'especialidad': r[10],
            'nombre_cliente': r[11]
        }
    except Exception as e:
        print(f"Error detallado: {str(e)}")  # Para debugging
        raise HTTPException(status_code=500, detail="Error al obtener la cita")

@citaRouter.get("/disponibilidad", status_code=status.HTTP_200_OK)
async def obtener_disponibilidad(fecha: str):
    """
    Obtiene la disponibilidad de empleados para una fecha específica
    """
    try:
        # Validar formato de fecha
        try:
            fecha_dt = datetime.strptime(fecha, '%Y-%m-%d')
            if fecha_dt.date() < datetime.now().date():
                raise HTTPException(status_code=400, detail="Fecha pasada no permitida")
        except ValueError:
            raise HTTPException(status_code=400, detail="Formato de fecha inválido. Use YYYY-MM-DD")
        
        # Obtener disponibilidad de empleados
        cleverCursor.execute('''
            SELECT e.id_empleado, e.nombre, e.especialidad,
                   d.hora, d.estado as disponible
            FROM empleados e
            LEFT JOIN disponibilidad d ON e.id_empleado = d.id_empleado AND d.fecha = %s
            WHERE e.estado = 1
            ORDER BY e.nombre, d.hora
        ''', (fecha_dt.strftime('%Y-%m-%d'),))
        
        disponibilidad = cleverCursor.fetchall()
        if not disponibilidad:
            return []  # Retornar lista vacía en lugar de error 404
            
        # Formatear los resultados
        disponibilidad_formateada = []
        for disp in disponibilidad:
            try:
                disponibilidad_formateada.append({
                    'id_empleado': disp[0],
                    'nombre': disp[1],
                    'especialidad': disp[2],
                    'hora': disp[3].strftime('%H:%M') if disp[3] else None,
                    'disponible': disp[4]
                })
            except Exception as e:
                print(f"Error formateando disponibilidad: {str(e)}")
                continue
        return disponibilidad_formateada
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        print(f"Error detallado: {str(e)}")  # Para debugging
        raise HTTPException(status_code=500, detail="Error al obtener disponibilidad")

@citaRouter.post("/", status_code=status.HTTP_201_CREATED)
def crear_cita(cita: CitaBase):
    try:
        cleverCursor.execute('''
            SELECT COUNT(*) FROM citas 
            WHERE fecha = %s AND hora = %s AND id_empleado = %s
        ''', (cita.fecha, cita.hora, cita.id_empleado))
        if cleverCursor.fetchone()[0] > 0:
            raise HTTPException(status_code=400, detail="Ya hay una cita en ese horario")

        cleverCursor.execute('''
            SELECT COUNT(*) FROM disponibilidad 
            WHERE fecha = %s AND hora = %s AND id_empleado = %s AND estado = 1
        ''', (cita.fecha, cita.hora, cita.id_empleado))
        if cleverCursor.fetchone()[0] == 0:
            raise HTTPException(status_code=400, detail="Horario no disponible")

        cleverCursor.execute('''
            INSERT INTO citas (id_cliente, id_empleado, id_servicio, fecha, hora, estado, notas)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        ''', (cita.id_cliente, cita.id_empleado, cita.id_servicio,
              cita.fecha, cita.hora, cita.estado, cita.notas))
        cleverCursor.execute('''
            UPDATE disponibilidad SET estado = 0 
            WHERE fecha = %s AND hora = %s AND id_empleado = %s
        ''', (cita.fecha, cita.hora, cita.id_empleado))
        mysqlConn.commit()
        return {"message": "Cita creada exitosamente"}
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al crear cita: {e}")

@citaRouter.put("/{id_cita}", status_code=status.HTTP_200_OK)
def actualizar_estado_cita(id_cita: int, estado: str):
    try:
        cleverCursor.execute("UPDATE citas SET estado = %s WHERE id_cita = %s", (estado, id_cita))
        mysqlConn.commit()
        return {"message": "Estado de la cita actualizado"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al actualizar estado: {e}")

@citaRouter.delete("/{id_cita}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_cita(id_cita: int):
    try:
        cleverCursor.execute("SELECT * FROM citas WHERE id_cita = %s", (id_cita,))
        if not cleverCursor.fetchone():
            raise HTTPException(status_code=404, detail="Cita no encontrada")
        cleverCursor.execute("DELETE FROM citas WHERE id_cita = %s", (id_cita,))
        mysqlConn.commit()
        return {"message": "Cita eliminada"}
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al eliminar cita: {e}")

