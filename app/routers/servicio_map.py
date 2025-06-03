from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List

class Servicio(BaseModel):
    id: int
    nombre: str
    descripcion: str
    precio: float

servicioRouter = APIRouter()

servicios_db = [
    Servicio(id=1, nombre="Corte de cabello", descripcion="Corte para hombres y mujeres", precio=15.0),
    Servicio(id=2, nombre="Manicura", descripcion="Manicura básica", precio=10.0),
]

@servicioRouter.get("/", response_model=List[Servicio])
async def listar_servicios():
    return servicios_db

@servicioRouter.get("/{servicio_id}", response_model=Servicio)
async def obtener_servicio(servicio_id: int):
    for servicio in servicios_db:
        if servicio.id == servicio_id:
            return servicio
    raise HTTPException(status_code=404, detail="Servicio no encontrado")

@servicioRouter.post("/", response_model=Servicio, status_code=201)
async def crear_servicio(servicio: Servicio):
    for s in servicios_db:
        if s.id == servicio.id:
            raise HTTPException(status_code=400, detail="El ID del servicio ya existe")
    servicios_db.append(servicio)
    return servicio
