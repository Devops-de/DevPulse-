from fastapi import APIRouter
from app.api.v1.endpoints import health, metrics

api_router = APIRouter()

# Register endpoint routers
api_router.include_router(health.router, tags=["Health"])
api_router.include_router(metrics.router, prefix="/metrics", tags=["Metrics & Pulse"])
