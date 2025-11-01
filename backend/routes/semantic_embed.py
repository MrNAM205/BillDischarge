from fastapi import APIRouter
from pydantic import BaseModel
from agents.SemanticOverlayEmbedder import embed_rebuttals

router = APIRouter()

class EmbedRequest(BaseModel):
  content: str

@router.post("/semantic/embed")
def embed_semantic_overlay(req: EmbedRequest):
  embedded = embed_rebuttals(req.content)
  return { "embeddedContent": embedded }