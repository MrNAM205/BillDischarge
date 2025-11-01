
from fastapi import APIRouter
from pydantic import BaseModel
from backend.agents.ManifestPublishAgent import publish_manifest

router = APIRouter()

class PublishRequest(BaseModel):
  filename: str
  registryUrl: str

@router.post("/trust/manifest/publish")
def publish_manifest_route(req: PublishRequest):
  receipt = publish_manifest(req.filename, req.registryUrl)
  return { "receipt": receipt }
