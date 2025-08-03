import logging

from fastapi import APIRouter
from starlette.responses import JSONResponse

from src.api.models.health_check import (
    ConnectionStatus,
    HealthCheckResponse,
    LivenessResponse,
)

logger = logging.getLogger(__name__)


health_check_router = APIRouter(tags=["Health check"])


@health_check_router.get("/liveness")
async def liveness() -> LivenessResponse:
    return LivenessResponse()


@health_check_router.get("/health")
async def health_check() -> JSONResponse:
    logger.info("Health check requested")

    third_party = ConnectionStatus.OK

    response = HealthCheckResponse(third_party=third_party)

    return JSONResponse(status_code=response.get_http_response_code(), content=response.model_dump())
