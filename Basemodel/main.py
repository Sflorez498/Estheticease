from typing import Union
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Importar routers modulares
from cliente_map import clienteRouter
from Basemodel.Servicos_map import servicoRouter
from producto_map import ProductoRouter
from Basemodel.venta_map import VentaRouter
from Basemodel.cita_map import citaRouter
# from usuario_map import usuarioRouter  # Descomentar si es necesario

# Crear instancia de la app
app = FastAPI()

# Incluir routers externos (modularización por entidad)
app.include_router(clienteRouter)
app.include_router(servicoRouter)
app.include_router(ProductoRouter)
app.include_router(VentaRouter)
app.include_router(citaRouter)
# app.include_router(usuarioRouter)  # Descomentar si lo necesitas

# Configuración de CORS
origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ruta raíz
@app.get("/")
async def read_root():
    return {"Hello": "World"}

# Ruta con parámetro de consulta opcional (query parameter)
# Ejemplo: /items/query?q=info
@app.get("/items/query")
async def read_query_param(q: Union[str, None] = None):
    return {"q": q}

# Ruta con parámetro en la URL (path parameter)
# Ejemplo: /items/5
@app.get("/items/{item_id}")
async def read_path_param(item_id: int):
    return {"item_id": item_id}

# Ruta combinada: path + query
# Ejemplo: /items/details/5?q=algo
@app.get("/items/details/{item_id}")
async def read_path_and_query(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

# Ruta para eliminar un ítem
# Ejemplo: DELETE /items_del/5
@app.delete("/items_del/{item_id}")
async def delete_by_id(item_id: int):
    return {"resultado": f"Se ha eliminado correctamente el item con ID {item_id}"}
