from fastapi import APIRouter
from api.v1.endpoints import patient, data_integration, simulation

api_router = APIRouter()
api_router.include_router(patient.router, prefix="/patients", tags=["patients"])
api_router.include_router(
    data_integration.router,
    prefix="/data-integration",
    tags=["data-integration"]
)
api_router.include_router(simulation.router, prefix="/simulation", tags=["simulation"]) 