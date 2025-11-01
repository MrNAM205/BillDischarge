from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from agents.JurisdictionalOverlayAgent import create_overlay

router = APIRouter()

class OverlayRequest(BaseModel):
  venue: str
  rebuttals: List[str]

@router.post("/jurisdictional/overlay")
def apply_overlay_route(req: OverlayRequest):
  overlay = create_overlay(req.venue, req.rebuttals)
  return { "overlay": overlay }