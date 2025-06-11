from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Importar routers modulares usando importaciones absolutas
from app.routers.cliente_map import clienteRouter
from app.routers.servicio_map import servicioRouter
from app.routers.producto_map import productoRouter
from app.routers.venta_map import ventaRouter
from app.routers.cita_map import citaRouter
from app.routers.empleado_map import empleadoRouter

# Importar routers modulares usando importaciones absolutas
from app.routers.admin import router as adminRouter  # Nuevo router de administración
# from routers.usuario_map import usuarioRouter  # Activar si se implementa
from app.routers.dev_map import devRouter  # Rutas de desarrollo separadas

# Configuración inicial de la API
app = FastAPI(
    title="Estheticease API",
    description="API para el sistema de gestión de salón de belleza Estheticease",
    version="1.0.0"
)

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar los orígenes permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar routers principales
app.include_router(clienteRouter, prefix="/api/clientes", tags=["Clientes"])
app.include_router(servicioRouter, prefix="/api/servicios", tags=["Servicios"])
app.include_router(productoRouter, prefix="/api/productos", tags=["Productos"])
app.include_router(ventaRouter, prefix="/api/ventas", tags=["Ventas"])
app.include_router(citaRouter, prefix="/api/citas", tags=["Citas"])
app.include_router(empleadoRouter, prefix="/api/empleados", tags=["Empleados"])
app.include_router(adminRouter)  # Router de administración
# app.include_router(usuarioRouter, prefix="/usuarios", tags=["Usuarios"])

# Rutas de prueba solo en desarrollo
app.include_router(devRouter, prefix="/dev", tags=["Desarrollo"])

# Ruta raíz GET
@app.get("/")
async def root():
    return {"message": "Bienvenido a la API de Estheticease"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
