from fastapi import APIRouter
from app.models.simple_model import SimpleResponse

simple_router = APIRouter()

@simple_router.get("/")
async def root():
    return SimpleResponse(
        message="¡Hola! Bienvenido a Estheticease",
        success=True,
        data={"version": "1.0"}
    )
