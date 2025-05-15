from fastapi import APIRouter

from app.api.endpoints import clientes
from app.core.config import settings

api_router = APIRouter()

# Include routers from endpoint modules
api_router.include_router(
    clientes.router, prefix="/clients", tags=["clients"]
)

# Health check endpoint
api_router.get("/health", tags=["health"])(lambda: {"status": "healthy"})