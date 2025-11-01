from fastapi import APIRouter
from pydantic import BaseModel
from agents.StatusDeclarationAgent import create_declaration

router = APIRouter()

class DeclarationRequest(BaseModel):
  fullName: str
  birthState: str
  signer: str
  jurisdiction: str
  privateKey: str

@router.post("/status/declaration")
def declare_status_route(req: DeclarationRequest):
  declaration = create_declaration(req.fullName, req.birthState, req.signer, req.jurisdiction, req.privateKey)
  return { "declaration": declaration }