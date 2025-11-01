from fastapi import APIRouter
from pydantic import BaseModel
from agents.CognitiveOverlayAgent import scan_and_inject

router = APIRouter()

class ScanRequest(BaseModel):
  content: str

@router.post("/cognitive/scan")
def scan_cognitive_overlay(req: ScanRequest):
  overlay = scan_and_inject(req.content)
  return { "overlay": overlay }