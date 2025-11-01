
from fastapi import APIRouter
from pydantic import BaseModel
from packages.EndorserKit.endorsement_engine import apply_endorsement

router = APIRouter()

class EndorsementRequest(BaseModel):
    parsedBill: dict
    templateName: str
    signer: str
    jurisdiction: str
    privateKey: str

@router.post("/endorse")
def endorse_bill(req: EndorsementRequest):
    signed = apply_endorsement(
        bill=req.parsedBill,
        template=req.templateName,
        signer=req.signer,
        jurisdiction=req.jurisdiction,
        private_key=req.privateKey
    )
    return {
        "signedEndorsement": signed,
        "telemetry": {
            "event": "endorsement_applied",
            "timestamp": signed["timestamp"],
            "signer": req.signer,
            "template": req.templateName
        }
    }
