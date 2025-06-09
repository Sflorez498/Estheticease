from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Importar routers modulares usando importaciones absolutas
from routers.cliente_map import clienteRouter
from routers.servicio_map import servicioRouter
from routers.producto_map import productoRouter
from routers.venta_map import ventaRouter
from routers.cita_map import citaRouter
# from routers.usuario_map import usuarioRouter  # Activar si se implementa
from routers.dev_map import devRouter  # Rutas de desarrollo separadas

# Configuración inicial de la API
app = FastAPI(
    title="API Spa Estheticease",
    description="Backend para clientes, servicios, productos, ventas y citas.",
    version="1.0.0",
    contact={"name": "Spa Estheticease", "email": "contacto@spa.com"}
)

# Orígenes permitidos para CORS (frontend)
origins = [
    "http://localhost:3000",
    "http://localhost:5173",  # Vite development server
    "http://localhost:8000",  # Backend
    "https://tu-frontend-en-produccion.com"
]

# Middleware de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar routers principales
app.include_router(clienteRouter, prefix="/clientes", tags=["Clientes"])
app.include_router(servicioRouter, prefix="/servicios", tags=["Servicios"])
app.include_router(productoRouter, prefix="/productos", tags=["Productos"])
app.include_router(ventaRouter, prefix="/ventas", tags=["Ventas"])
app.include_router(citaRouter, prefix="/citas", tags=["Citas"])
# app.include_router(usuarioRouter, prefix="/usuarios", tags=["Usuarios"])

# Rutas de prueba solo en desarrollo
app.include_router(devRouter, prefix="/dev", tags=["Desarrollo"])

# Ruta raíz GET
@app.get("/")
async def read_root():
    return {"message": "Bienvenido a la API de Estheticease"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
