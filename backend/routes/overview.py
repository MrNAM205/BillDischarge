
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

# In-memory storage for project overview
project_overview = {
    "goals": "Manage sovereign cognition, remedy protocols, and financial discharge workflows.",
    "pain_points": "Lack of a centralized system to track and manage these complex processes.",
    "agent_ancestry": "Built on the Gemini platform."
}

class ProjectOverview(BaseModel):
    goals: str
    pain_points: str
    agent_ancestry: str

@router.get("/project_overview", response_model=ProjectOverview)
async def get_project_overview():
    """
    Retrieve the project overview, including goals, pain points, and agent ancestry.
    """
    return project_overview

@router.post("/project_overview", response_model=ProjectOverview)
async def update_project_overview(overview: ProjectOverview):
    """
    Update the project overview.
    """
    project_overview.update(overview.dict())
    return project_overview
