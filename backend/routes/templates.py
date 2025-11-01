
from fastapi import APIRouter
from packages.EndorserKit.utils import load_endorsement_templates

router = APIRouter()

@router.get("/endorsement-templates")
def get_endorsement_templates():
    templates_dir = "config/endorsement_templates"
    templates = load_endorsement_templates(templates_dir)
    return templates
