from typing import Any, Dict

from fastapi import APIRouter

router = APIRouter()


@router.get("/project")
async def get_project_overview() -> Dict[str, Any]:
    """
    Returns a structured overview of the project.
    """
    project_overview = {
        "summary": "A sovereign financial cockpit—a modular system for managing legal status correction, remedy protocols, and financial instruments.",
        "goals": [
            "Modularize cognition into sovereign agents",
            "Improve maintainability via FastAPI + Poetry",
            "Add fallback logic for local models",
            "Scaffold narratable remedy protocols",
            "Integrate frontend with backend cognition",
        ],
        "pain_points": [
            "Gemini injecting institutional disclaimers",
            "Port conflicts and backend startup failures",
            "YAML parse errors in agent config",
            "Lack of dynamic fallback between models",
            "Incomplete frontend-agent integration",
        ],
        "agent_lineage": "Omni2 - A cognition agent that scaffolds lawful remedy, annotates contradictions, and supports sovereign authorship.",
    }
    return project_overview
