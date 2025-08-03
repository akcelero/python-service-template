from fastapi import APIRouter

from src.api.health_check import health_check_router

router_api = APIRouter(prefix="/api/v1")
router_api.include_router(health_check_router)
