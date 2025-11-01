from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from agents.SovereignInvocationAgent import create_sovereign_manifest

router = APIRouter()

class InvocationRequest(BaseModel):
  content: str
  fullName: str
  birthState: str
  signer: str
  jurisdiction: str
  venue: str
  rebuttals: List[str]

@router.post("/sovereign/invoke")
def invoke_sovereign_manifest_route(req: InvocationRequest):
  manifest = create_sovereign_manifest(
      req.content,
      req.fullName,
      req.birthState,
      req.signer,
      req.jurisdiction,
      req.venue,
      req.rebuttals
  )
  return { "manifest": manifest }