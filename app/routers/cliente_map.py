from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from database.Clever_MySQL_conn import cleverCursor, mysqlConn
import bcrypt
from typing import List, Optional

clienteRouter = APIRouter()

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

@clienteRouter.post("/clientes/", status_code=status.HTTP_201_CREATED)
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

@clienteRouter.get("/clientes/", status_code=status.HTTP_200_OK)
def get_all_clients() -> List[dict]:
    try:
        cleverCursor.execute(
            "SELECT Id_Cliente, Nombre, Contacto, Correo, Genero, Edad FROM Clientes"
        )
        clientes = cleverCursor.fetchall()
        return clientes
    except Exception as err:
        raise HTTPException(status_code=500, detail=f"Error al obtener los clientes: {err}")

@clienteRouter.get("/clientes/{id_cliente}", status_code=status.HTTP_200_OK)
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

@clienteRouter.post("/login/", status_code=status.HTTP_200_OK)
def login_user(creenciales: CredencialesLogin):
    try:
        cleverCursor.execute(
            "SELECT * FROM Clientes WHERE Correo = %s", (creenciales.correo,)
        )
        user = cleverCursor.fetchone()
        if not user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
        hashed_password_from_db = user[4]  # Verifica este índice según tu tabla
        
        if bcrypt.checkpw(creenciales.contraseña.encode('utf-8'), hashed_password_from_db.encode('utf-8')):
            return {"message": "Inicio de sesión exitoso"}
        else:
            raise HTTPException(status_code=401, detail="Contraseña incorrecta")
    except Exception as err:
        raise HTTPException(status_code=500, detail=f"Error al iniciar sesión: {err}")

# Nueva ruta para eliminar un cliente
@clienteRouter.delete("/clientes/{id_cliente}", status_code=status.HTTP_204_NO_CONTENT)
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
