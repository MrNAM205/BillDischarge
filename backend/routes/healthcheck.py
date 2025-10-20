
from fastapi import APIRouter

router = APIRouter()

@router.get("/healthcheck")
async def healthcheck():
    """
    Healthcheck endpoint to verify that the backend is running.
    """
    return {"status": "ok"}
