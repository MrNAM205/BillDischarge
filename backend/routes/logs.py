from fastapi import APIRouter
from typing import List, Dict, Any

router = APIRouter()

# In-memory journal for remedy logs
remedy_journal: List[Dict[str, Any]] = []

@router.get("/remedy_logs", response_model=List[Dict[str, Any]])
async def get_remedy_logs():
    """
    Retrieve the remedy journal, which logs every cognition loop, fallback trace, and model lineage.
    """
    return remedy_journal

def log_remedy_action(action: str, details: Dict[str, Any]):
    """
    Log an action to the remedy journal.
    """
    remedy_journal.append({"action": action, "details": details})