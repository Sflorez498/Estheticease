# Archivo principal de la API FastAPI
# Configuración y registro de rutas para el sistema de gestión de salón de belleza

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Importar routers para cada módulo de la aplicación
# Cada router maneja una funcionalidad específica
from app.routers.cita_map import citaRouter as cita_router  # Rutas para citas
from app.routers.cliente_map import clienteRouter as cliente_router  # Rutas para clientes
from app.routers.servicio_map import servicioRouter as servicio_router  # Rutas para servicios
from app.routers.admin import router as adminRouter  # Rutas para administración
from app.routers.dev_map import devRouter as dev_router  # Rutas para desarrollo
from app.routers.producto_map import productoRouter as producto_router  # Rutas para productos
from app.routers.venta_map import ventaRouter as venta_router  # Rutas para ventas
from app.routers.empleado_map import empleadoRouter as empleado_router  # Rutas para empleados

# Inicialización de la aplicación FastAPI
app = FastAPI(
    title="Estheticease API",
    description="API para el sistema de gestión de salón de belleza Estheticease",
    version="1.0.0"
)

# Configuración de CORS para permitir peticiones desde el frontend
# Esto permite que el frontend pueda hacer peticiones al backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite peticiones desde cualquier origen
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos HTTP
    allow_headers=["*"],  # Permite todos los headers
)

# Registro de rutas de la aplicación
# Cada ruta tiene un prefijo que indica su funcionalidad
app.include_router(cliente_router, prefix="/api/clientes", tags=["Clientes"])  # Rutas para clientes
app.include_router(servicio_router, prefix="/api/servicios", tags=["Servicios"])  # Rutas para servicios
app.include_router(cita_router, prefix="/api/citas", tags=["Citas"])  # Rutas para citas
app.include_router(adminRouter, prefix="/admin", tags=["Admin"])  # Rutas de administración
app.include_router(dev_router, prefix="/dev", tags=["Dev"])  # Rutas de desarrollo
app.include_router(producto_router, prefix="/api/productos", tags=["Productos"])  # Rutas para productos
app.include_router(venta_router, prefix="/api/ventas", tags=["Ventas"])  # Rutas para ventas
app.include_router(empleado_router, prefix="/api/empleados", tags=["Empleados"])  # Rutas para empleados

# Ruta raíz de la API
@app.get("/")
async def root():
    """Endpoint raíz que muestra un mensaje de bienvenida a la API"""
    return {"message": "Bienvenido a la API de Estheticease"}

# Configuración para ejecutar el servidor
if __name__ == "__main__":
    # Iniciar el servidor cuando se ejecuta el archivo directamente
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)  # Ejecuta el servidor en el puerto 8000
