
from fastapi import APIRouter
from pydantic import BaseModel
from backend.agents.ManifestSignAgent import sign_manifest

router = APIRouter()

class SignRequest(BaseModel):
  filename: str
  privateKey: str

@router.post("/trust/manifest/sign")
def sign_manifest_route(req: SignRequest):
  signed = sign_manifest(req.filename, req.privateKey)
  return { "signedManifest": signed }
