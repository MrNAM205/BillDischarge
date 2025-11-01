from fastapi import APIRouter
from pydantic import BaseModel
from agents.SemanticOverlayAuditor import audit_semantics

router = APIRouter()

class AuditRequest(BaseModel):
  content: str

@router.post("/semantic/audit")
def audit_semantic_overlay(req: AuditRequest):
  report = audit_semantics(req.content)
  return { "report": report }