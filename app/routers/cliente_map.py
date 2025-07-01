# Módulo que maneja todas las operaciones relacionadas con clientes
# Incluye registro, login, actualización y eliminación de clientes

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from ..database.Clever_MySQL_conn import cleverCursor, mysqlConn
import bcrypt
from typing import List, Optional

# Creación del router para rutas de clientes
clienteRouter = APIRouter()

# Modelo de datos para un cliente
# Define la estructura que debe seguir cada cliente
# Incluye validación automática de tipos
class ClienteDB(BaseModel):
    nombre: str  # Nombre completo del cliente
    contacto: str  # Teléfono o información de contacto
    correo: str  # Email del cliente
    contraseña: str  # Contraseña (se guarda encriptada)
    genero: str  # Género del cliente
    edad: int  # Edad del cliente

class CredencialesLogin(BaseModel):
    correo: str  # Email para login
    contraseña: str  # Contraseña para login

# Ruta para crear un nuevo cliente
# Recibe datos del cliente y lo registra en la base de datos
# La contraseña se guarda encriptada para seguridad
@clienteRouter.post("/", status_code=status.HTTP_201_CREATED)
def registrar_cliente(clientePost: ClienteDB):
    """
    Registra un nuevo cliente en el sistema
    - Encripta la contraseña antes de guardar
    - Retorna mensaje de éxito o error
    """
    try:
        # Encriptar la contraseña
        hashed_password = bcrypt.hashpw(clientePost.contraseña.encode('utf-8'), bcrypt.gensalt())
        
        # Consulta SQL para insertar el nuevo cliente
        insert_query = """
        INSERT INTO Clientes (Nombre, Contacto, Correo, Contraseña, Genero, Edad)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        
        # Valores a insertar
        values = (
            clientePost.nombre,
            clientePost.contacto,
            clientePost.correo,
            hashed_password.decode('utf-8'),
            clientePost.genero,
            clientePost.edad
        )
        
        # Ejecutar consulta y confirmar cambios
        cleverCursor.execute(insert_query, values)
        mysqlConn.commit()
        
        return {"message": "Cliente registrado correctamente"}
    except Exception as err:
        raise HTTPException(status_code=400, detail=f"Error al registrar cliente: {err}")

# Ruta para obtener todos los clientes
# Retorna una lista con todos los clientes registrados
@clienteRouter.get("/", status_code=status.HTTP_200_OK)
def get_all_clients() -> List[dict]:
    """
    Obtiene la lista de todos los clientes
    - Retorna datos básicos de cada cliente
    - No incluye contraseñas en los resultados
    """
    try:
        cleverCursor.execute(
            "SELECT Id_Cliente, Nombre, Contacto, Correo, Genero, Edad FROM Clientes"
        )
        clientes = cleverCursor.fetchall()
        return clientes
    except Exception as err:
        raise HTTPException(status_code=500, detail=f"Error al obtener clientes: {err}")

# Ruta para obtener un cliente específico
# Busca un cliente por su ID y retorna sus datos
@clienteRouter.get("/{id_cliente}", status_code=status.HTTP_200_OK)
def get_cliente_by_id(id_cliente: int) -> Optional[dict]:
    """
    Busca un cliente por su ID
    - Retorna datos completos del cliente
    - Retorna 404 si no se encuentra
    """
    try:
        cleverCursor.execute(
            "SELECT Id_Cliente, Nombre, Contacto, Correo, Genero, Edad FROM Clientes WHERE Id_Cliente = %s",
            (id_cliente,)
        )
        cliente = cleverCursor.fetchone()
        if cliente:
            return cliente
        else:
            raise HTTPException(status_code=404, detail="Cliente no encontrado")
    except Exception as err:
        raise HTTPException(status_code=500, detail=f"Error al buscar cliente: {err}")

# Ruta para iniciar sesión
# Verifica las credenciales del usuario
@clienteRouter.post("/login", status_code=status.HTTP_200_OK)
def login_user(creenciales: CredencialesLogin):
    """
    Proceso de login de un cliente
    - Verifica correo y contraseña
    - Retorna ID del cliente si las credenciales son correctas
    """
    try:
        cleverCursor.execute(
            "SELECT Id_Cliente, Nombre, Contacto, Correo, Contraseña, Genero, Edad FROM Clientes WHERE Correo = %s", 
            (creenciales.correo,)
        )
        user = cleverCursor.fetchone()
        if not user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
        # Verificar contraseña
        hashed_password_from_db = user[4]
        if bcrypt.checkpw(creenciales.contraseña.encode('utf-8'), hashed_password_from_db.encode('utf-8')):
            return {"message": "Inicio de sesión exitoso", "Id_Cliente": user[0]}
        else:
            raise HTTPException(status_code=401, detail="Contraseña incorrecta")
    except Exception as err:
        print(f"Error en login: {str(err)}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")

# Ruta para actualizar datos de un cliente
@clienteRouter.put("/{id_cliente}", status_code=status.HTTP_200_OK)
def actualizar_cliente(id_cliente: int, cliente: ClienteDB):
    """
    Actualiza los datos de un cliente existente
    - Actualiza todos los campos del cliente
    - La nueva contraseña se encripta antes de guardar
    """
    try:
        update_query = """
        UPDATE Clientes 
        SET Nombre = %s, Contacto = %s, Correo = %s, 
            Contraseña = %s, Genero = %s, Edad = %s
        WHERE Id_Cliente = %s
        """
        
        # Encriptar la nueva contraseña
        hashed_password = bcrypt.hashpw(cliente.contraseña.encode('utf-8'), bcrypt.gensalt())
        
        values = (
            cliente.nombre,
            cliente.contacto,
            cliente.correo,
            hashed_password.decode('utf-8'),
            cliente.genero,
            cliente.edad,
            id_cliente
        )
        
        cleverCursor.execute(update_query, values)
        mysqlConn.commit()
        
        return {"message": "Datos actualizados correctamente"}
    except Exception as err:
        raise HTTPException(status_code=500, detail=f"Error al actualizar datos: {err}")

# Ruta para eliminar un cliente
@clienteRouter.delete("/{id_cliente}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_cliente(id_cliente: int):
    try:
        # Verificar si el cliente existe antes de intentar eliminarlo
        cleverCursor.execute(
            "SELECT * FROM Clientes WHERE Id_Cliente = %s", (id_cliente,)
        )
        cliente = cleverCursor.fetchone()
        if not cliente:
            raise HTTPException(status_code=404, detail="Cliente no encontrado")

        # Eliminar el cliente
        delete_query = "DELETE FROM Clientes WHERE Id_Cliente = %s"
        cleverCursor.execute(delete_query, (id_cliente,))
        mysqlConn.commit()
        return {"message": "Cliente eliminado exitosamente"}
    except Exception as err:
        raise HTTPException(status_code=500, detail=f"Error al eliminar cliente: {err}")
