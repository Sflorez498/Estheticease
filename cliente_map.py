from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from Clever_MySQL_conn import cleverCursor, mysqlConn

clienteRouter = APIRouter()

class ClienteDB(BaseModel):
    nombre: str
    contacto: str  # Teléfono
    correo: str
    contraseña: str
    genero: str
    edad: int

class CredencialesLogin(BaseModel):
    Correo: str
    Contraseña: str

# POST - Registrar nuevo cliente (sin cambios)
@clienteRouter.post("/clientes/", status_code=status.HTTP_201_CREATED)
def insert_user(clientePost: ClienteDB):
    insert_query = """
    INSERT INTO Clientes (Nombre, Contacto, Correo, Contraseña, Genero, Edad)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    values = (
        clientePost.nombre,
        clientePost.contacto,
        clientePost.correo,
        clientePost.contraseña,
        clientePost.genero,
        clientePost.edad
    )

    try:
        cleverCursor.execute(insert_query, values)
        mysqlConn.commit()
        return {"message": "Cliente insertado correctamente"}
    except Exception as err:
        raise HTTPException(status_code=400, detail=f"Error al registrar cliente: {err}")

# GET - Obtener todos los clientes (sin cambios)
@clienteRouter.get("/clientes/", status_code=status.HTTP_200_OK)
def get_all_clients():
    try:
        cleverCursor.execute("SELECT * FROM Clientes")
        clientes = cleverCursor.fetchall()
        return clientes
    except Exception as err:
        raise HTTPException(status_code=500, detail=f"Error al obtener los clientes: {err}")

# GET - Obtener cliente por ID (sin cambios)
@clienteRouter.get("/clientes/{id_cliente}", status_code=status.HTTP_200_OK)
def get_cliente_by_id(id_cliente: int):
    try:
        cleverCursor.execute("SELECT * FROM Clientes WHERE Id_Cliente = %s", (id_cliente,))
        cliente = cleverCursor.fetchone()
        if cliente:
            return cliente
        else:
            raise HTTPException(status_code=404, detail="Cliente no encontrado")
    except Exception as err:
        raise HTTPException(status_code=500, detail=f"Error al buscar cliente: {err}")

# POST - Iniciar sesión
@clienteRouter.post("/login/")
def login_user(creenciales: CredencialesLogin):
    try:
        cleverCursor.execute("SELECT * FROM Clientes WHERE Correo = %s", (creenciales.Correo,))
        user = cleverCursor.fetchone()

        if user:
            # ¡PELIGRO! En producción, NUNCA compares contraseñas directamente.
            # Debes usar una biblioteca para hashear y verificar contraseñas (como bcrypt).
            if user[4] == creenciales.Contraseña:  # Asumiendo que la contraseña está en la quinta columna (índice 4)
                return {"message": "Inicio de sesión exitoso"}
            else:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Contraseña incorrecta")
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
    except Exception as err:
        raise HTTPException(status_code=status.HTTP_500, detail=f"Error al iniciar sesión: {err}")