from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from app.database.Clever_MySQL_conn import cleverCursor, mysqlConn
from typing import Optional

class EmpleadoBase(BaseModel):
    nombre: str
    especialidad: str
    correo: str
    telefono: str
    direccion: str

class Empleado(EmpleadoBase):
    id_empleado: Optional[int] = None

empleadoRouter = APIRouter()

@empleadoRouter.get("/", status_code=status.HTTP_200_OK)
async def obtener_empleados():
    try:
        print("Consultando lista de empleados")
        cleverCursor.execute('''
            SELECT Id_Empleado, nombre, correo, telefono, especialidad, direccion, estado 
            FROM empleados 
            WHERE estado = 1
            ORDER BY nombre
        ''')
        empleados = cleverCursor.fetchall()
        print(f"Encontrados {len(empleados)} empleados activos")

        if not empleados:
            return []  # Retornar lista vacía en lugar de error 404

        empleados_formateados = []
        for e in empleados:
            try:
                empleado = {
                    'id_empleado': e[0],
                    'nombre': e[1],
                    'correo': e[2],
                    'telefono': e[3],
                    'especialidad': e[4],
                    'direccion': e[5],
                    'estado': e[6]
                }
                empleados_formateados.append(empleado)
            except Exception as e:
                print(f"Error formateando empleado {e[0]}: {str(e)}")
                continue
        
        return empleados_formateados
    except mysql.connector.Error as sql_err:
        print(f"Error MySQL: {sql_err}")
        raise HTTPException(status_code=500, detail=f"Error MySQL: {sql_err}")
    except Exception as e:
        print(f"Error inesperado: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")

@empleadoRouter.get("/{id_empleado}", status_code=status.HTTP_200_OK)
async def obtener_empleado_por_id(id_empleado: int):
    if id_empleado <= 0:
        raise HTTPException(status_code=400, detail="ID inválido")

    try:
        cleverCursor.execute('''
            SELECT Id_Empleado, nombre, correo, telefono, especialidad, direccion, estado 
            FROM empleados 
            WHERE Id_Empleado = %s AND estado = 1
        ''', (id_empleado,))
        e = cleverCursor.fetchone()

        if not e:
            return None  # Retornar None en lugar de error 404

        return {
            'id_empleado': e[0],
            'nombre': e[1],
            'correo': e[2],
            'telefono': e[3],
            'especialidad': e[4],
            'direccion': e[5],
            'estado': e[6]
        }
    except Exception as e:
        print(f"Error detallado: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error al obtener empleado: {e}")

@empleadoRouter.post("/", status_code=status.HTTP_201_CREATED)
async def crear_empleado(empleado: EmpleadoBase):
    try:
        cleverCursor.execute('''
            INSERT INTO empleados (nombre, especialidad, correo, telefono, direccion, estado)
            VALUES (%s, %s, %s, %s, %s, 1)
        ''', (
            empleado.nombre,
            empleado.especialidad,
            empleado.correo,
            empleado.telefono,
            empleado.direccion
        ))
        mysqlConn.commit()
        return {"message": "Empleado creado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al crear empleado: {e}")

@empleadoRouter.put("/{empleado_id}", status_code=status.HTTP_200_OK)
async def actualizar_empleado(empleado_id: int, empleado: EmpleadoBase):
    try:
        cleverCursor.execute('''
            UPDATE empleados 
            SET nombre = %s, especialidad = %s, correo = %s, telefono = %s, direccion = %s
            WHERE id_empleado = %s
        ''', (
            empleado.nombre,
            empleado.especialidad,
            empleado.correo,
            empleado.telefono,
            empleado.direccion,
            empleado_id
        ))
        mysqlConn.commit()
        return {"message": "Empleado actualizado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al actualizar empleado: {e}")

@empleadoRouter.delete("/{empleado_id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_empleado(empleado_id: int):
    try:
        cleverCursor.execute('''
            UPDATE empleados 
            SET estado = 0 
            WHERE id_empleado = %s
        ''', (empleado_id,))
        mysqlConn.commit()
        return {"message": "Empleado desactivado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al desactivar empleado: {e}")
