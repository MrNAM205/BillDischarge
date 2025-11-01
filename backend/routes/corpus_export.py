
from fastapi import APIRouter
from pydantic import BaseModel
from backend.agents.CorpusExportAgent import export_manifest

router = APIRouter()

class ExportRequest(BaseModel):
  files: list[str]

@router.post("/trust/corpus/export")
def export_corpus_manifest(req: ExportRequest):
  manifest = export_manifest(req.files)
  return { "manifest": manifest }
