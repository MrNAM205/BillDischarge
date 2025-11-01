from fastapi import APIRouter
from pydantic import BaseModel
from agents.SemanticOverlayEngine import scan_content

router = APIRouter()

class ScanRequest(BaseModel):
  content: str

@router.post("/semantic/scan")
def scan_semantic_overlay(req: ScanRequest):
  flags = scan_content(req.content)
  return { "flags": flags }