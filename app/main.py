from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.cita_map import citaRouter as cita_router
from app.routers.cliente_map import clienteRouter as cliente_router
from app.routers.servicio_map import servicioRouter as servicio_router
from app.routers.admin import router as adminRouter
from app.routers.dev_map import devRouter as dev_router
from app.routers.producto_map import productoRouter as producto_router
from app.routers.venta_map import ventaRouter as venta_router
from app.routers.empleado_map import empleadoRouter as empleado_router

app = FastAPI(
    title="Estheticease API",
    description="API para el sistema de gestión de salón de belleza Estheticease",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registro de rutas
app.include_router(cliente_router, prefix="/api/clientes", tags=["Clientes"])
app.include_router(servicio_router, prefix="/api/servicios", tags=["Servicios"])
app.include_router(cita_router, prefix="/api/citas", tags=["Citas"])
app.include_router(adminRouter, prefix="/admin", tags=["Admin"])
app.include_router(dev_router, prefix="/dev", tags=["Dev"])
app.include_router(producto_router, prefix="/api/productos", tags=["Productos"])
app.include_router(venta_router, prefix="/api/ventas", tags=["Ventas"])
app.include_router(empleado_router, prefix="/api/empleados", tags=["Empleados"])

@app.get("/")
async def root():
    return {"message": "Bienvenido a la API de Estheticease"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
