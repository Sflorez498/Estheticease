# Importamos las librerías necesarias para la API y la base de datos
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from ..database.Clever_MySQL_conn import cleverCursor, mysqlConn
import bcrypt
from typing import List, Optional

clienteRouter = APIRouter()

# Clase que define el modelo de datos para un cliente
# Cada cliente debe tener:
# - nombre: nombre completo del cliente
# - contacto: número de teléfono o información de contacto
# - correo: dirección de correo electrónico
# - contraseña: contraseña para iniciar sesión
# - genero: género del cliente
# - edad: edad del cliente

class ClienteDB(BaseModel):
    nombre: str
    contacto: str
    correo: str
    contraseña: str
    genero: str
    edad: int

class CredencialesLogin(BaseModel):
    correo: str
    contraseña: str

# Ruta para registrar un nuevo cliente
# Recibe los datos del cliente y los guarda en la base de datos
# Retorna un mensaje de éxito si todo sale bien
@clienteRouter.post("/", status_code=status.HTTP_201_CREATED)
def registrar_cliente(clientePost: ClienteDB):
    try:
        hashed_password = bcrypt.hashpw(clientePost.contraseña.encode('utf-8'), bcrypt.gensalt())
        insert_query = """
        INSERT INTO Clientes (Nombre, Contacto, Correo, Contraseña, Genero, Edad)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        values = (
            clientePost.nombre,
            clientePost.contacto,
            clientePost.correo,
            hashed_password.decode('utf-8'),
            clientePost.genero,
            clientePost.edad
        )
        cleverCursor.execute(insert_query, values)
        mysqlConn.commit()
        return {"message": "Cliente insertado correctamente"}
    except Exception as err:
        raise HTTPException(status_code=400, detail=f"Error al registrar cliente: {err}")

# Ruta para obtener la lista de todos los clientes
# Retorna una lista con todos los clientes registrados
@clienteRouter.get("/", status_code=status.HTTP_200_OK)
def get_all_clients() -> List[dict]:
    try:
        cleverCursor.execute(
            "SELECT Id_Cliente, Nombre, Contacto, Correo, Genero, Edad FROM Clientes"
        )
        clientes = cleverCursor.fetchall()
        return clientes
    except Exception as err:
        raise HTTPException(status_code=500, detail=f"Error al obtener los clientes: {err}")

# Ruta para buscar un cliente por su ID
# Recibe el ID del cliente y retorna sus datos
# Si no encuentra el cliente, retorna un error 404
@clienteRouter.get("/{id_cliente}", status_code=status.HTTP_200_OK)
def get_cliente_by_id(id_cliente: int) -> Optional[dict]:
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

# Ruta para iniciar sesión de un cliente
# Verifica el correo y contraseña del cliente
# Si las credenciales son correctas, permite el acceso
@clienteRouter.post("/login", status_code=status.HTTP_200_OK)
def login_user(creenciales: CredencialesLogin):
    try:
        cleverCursor.execute(
            "SELECT Id_Cliente, Nombre, Contacto, Correo, Contraseña, Genero, Edad FROM Clientes WHERE Correo = %s", 
            (creenciales.correo,)
        )
        user = cleverCursor.fetchone()
        if not user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
        # La contraseña está en el índice 4 (según la consulta)
        hashed_password_from_db = user[4]
        
        if bcrypt.checkpw(creenciales.contraseña.encode('utf-8'), hashed_password_from_db.encode('utf-8')):
            return {"message": "Inicio de sesión exitoso", "Id_Cliente": user[0]}
        else:
            raise HTTPException(status_code=401, detail="Contraseña incorrecta")
    except Exception as err:
        print(f"Error en login: {str(err)}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")

# Nueva ruta para eliminar un cliente
# Ruta para eliminar un cliente
# Recibe el ID del cliente y lo elimina de la base de datos
# Si el cliente no existe, retorna un error 404
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
