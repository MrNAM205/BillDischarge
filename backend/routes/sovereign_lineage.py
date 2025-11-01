from fastapi import APIRouter, Body
from typing import Optional

from backend.agents.SovereignLineageAgent import SovereignLineageAgent

router = APIRouter()
lineage_agent = SovereignLineageAgent()

@router.post("/lineage/log")
async def log_invocation(
    module: str = Body(...),
    signer: str = Body(...),
    jurisdiction: str = Body(...),
    overlays: list = Body(...),
    manifest_hash: str = Body(...),
    exported: bool = Body(...),
    signed: bool = Body(...),
    published: bool = Body(...)
):
    """Logs a new invocation."""
    return lineage_agent.log_invocation(
        module, signer, jurisdiction, overlays, manifest_hash, exported, signed, published
    )

@router.get("/lineage/history")
async def get_history(module: Optional[str] = None, signer: Optional[str] = None):
    """Retrieves the full or filtered invocation history."""
    return lineage_agent.get_history(module, signer)
