from typing import Union
from fastapi import FastAPI
#from usuario_map import usuarioRouter
from cliente_map import clienteRouter
from Servicos_map import servicoRouter
from producto_map import ProductoRouter
from venta_map import VentaRouter
from cita_map import citaRouter
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
#app.include_router(usuarioRouter)
app.include_router(clienteRouter)
app.include_router(servicoRouter)
app.include_router(ProductoRouter)
app.include_router(VentaRouter)
app.include_router(citaRouter)


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


@app.get("/")
async def read_root():
    return {"Hello": "World"}

#solo parametro la url debe enviarse: "http://127.0.0.1:8000/items/?q=infoComoParametro"
@app.get("/items/")
async def read_param_item(q: Union[str, None] = None):
    return {"q": q}

#solo info como parte de la url debe enviarse: "http://127.0.0.1:8000/items/5"
@app.get("/items/{item_id}")
async def read_paramInPath_item(item_id: int):
    return {"item_id": item_id}

#realizar envio de información de las 2 formas en simultánea en la url debe enviarse: "http://127.0.0.1:8000/items/5?q=infoComoParametro"
@app.get("/items/{item_id}")
async def read_both_paramTypes_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
    
@app.delete("/items_del/{item_id}")
async def delete_by_id(item_id: int):
    return {"resultado": "Se ha eliminado correctamente el item solicitado"}
    