from fastapi import APIRouter
from backend.routes.remedy import last_remedy

router = APIRouter()


@router.get("/api/status", tags=["Status"])
async def get_status():
    """
    Reports the current operational state of the Omni2 agent,
    including the last model, thoughts, and any fallback from the remedy scaffolder.
    """
    return {
        "last_model": last_remedy["model"],
        "last_thoughts": last_remedy["thoughts"],
        "fallback": last_remedy.get("fallback", None),
        "status": "Operational",
    }
