import logging

from fastapi import APIRouter, Request, status

probe_route = APIRouter(
    tags=["probes"],
    responses={404: {"description": "Not found"}},
)
logger = logging.getLogger(__name__)


@probe_route.get("/")
async def health_check():
    """Used for load-balancer health-checks"""
    return status.HTTP_200_OK


@probe_route.get("/startup")
async def probe_startup(request: Request):
    """Used for startup probe"""
    try:
        _ = request.app.state
        return status.HTTP_200_OK
    except Exception as e:
        logger.warning(f"startup incomplete {e}")
        return status.HTTP_503_SERVICE_UNAVAILABLE


@probe_route.get("/readiness")
async def probe_readiness(request: Request):
    """Used for readiness probe"""
    try:
        if request.app.state:
            return status.HTTP_200_OK
        else:
            logger.warning("App is not ready")
            return status.HTTP_425_TOO_EARLY
    except Exception as e:
        logger.warning(f"startup incomplete {e}")
        return status.HTTP_503_SERVICE_UNAVAILABLE
