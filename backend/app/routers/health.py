from fastapi import APIRouter

from app.api import HealthResponse

health_router = APIRouter()


@health_router.get(
    "/health", summary="Health", response_model=HealthResponse, include_in_schema=False
)
async def check_health():
    """
    Check API health
    """
    return {"ok": True}
