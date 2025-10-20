from fastapi import APIRouter

router = APIRouter()

# Mock data for demonstration purposes
mock_fallback_data = {
    "fallback_count": 0,
    "last_fallback_timestamp": None,
    "status": "All systems nominal. No fallback events detected."
}

mock_cognition_lineage = [
    {
        "agent": "Omni2",
        "timestamp": "2025-10-15T10:00:00Z",
        "action": "Annotated Instrument #12345",
        "confidence": 0.98
    },
    {
        "agent": "LocalAgentCore",
        "timestamp": "2025-10-15T10:01:00Z",
        "action": "Detected contradiction: VOID",
        "confidence": 0.99
    }
]

@router.get("/api/cockpit/status", tags=["Cockpit"])
async def get_cockpit_status():
    """
    Aggregates and returns the operational status of the entire Sovereign Cognition system,
    including backend health, fallback status, and cognition lineage.
    """
    return {
        "health": {
            "status": "healthy",
            "timestamp": "2025-10-15T10:02:00Z",
            "services": {
                "annotator": "online",
                "pdf_endorser": "online",
                "remedy_logger": "online"
            }
        },
        "fallback_cognition": mock_fallback_data,
        "cognition_lineage": mock_cognition_lineage
    }
