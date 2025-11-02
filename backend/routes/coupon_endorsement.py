from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from agents.CouponEndorserAgent import endorse_coupon, endorse_bill, create_promissory_note, validate_negotiability

router = APIRouter()

class CouponEndorsementRequest(BaseModel):
    endorser_name: str = Field(..., description="Full name of the endorser")
    amount: str = Field(..., description="Coupon amount")
    payee: str = Field(..., description="Payee name")
    account_number: str = Field(..., description="Account number")
    endorsement_type: str = Field(..., description="Type of endorsement (private_trust, acceptance_for_value)")
    due_date: Optional[str] = Field(None, description="Due date if applicable")

class BillEndorsementRequest(BaseModel):
    endorser_name: str = Field(..., description="Full name of the endorser")
    amount: str = Field(..., description="Bill amount")
    creditor: str = Field(..., description="Creditor name")
    bill_number: str = Field(..., description="Bill number or reference")
    endorsement_type: Optional[str] = Field("private_trust", description="Type of endorsement")
    due_date: Optional[str] = Field(None, description="Due date if applicable")

class PromissoryNoteRequest(BaseModel):
    maker_name: str = Field(..., description="Name of the note maker")
    amount: str = Field(..., description="Note amount")
    payee: str = Field(..., description="Payee name")
    note_title: Optional[str] = Field("Promissory Note", description="Title of the note")
    due_date: Optional[str] = Field(None, description="Due date")
    payable_on_demand: Optional[bool] = Field(True, description="Payable on demand")
    jurisdiction: Optional[str] = Field("Common Law", description="Jurisdiction")

class NegotiabilityValidationRequest(BaseModel):
    document_type: str = Field(..., description="Type of document (coupon, bill, note)")
    amount: Optional[str] = Field(None, description="Document amount")
    payee: Optional[str] = Field(None, description="Payee name")
    due_date: Optional[str] = Field(None, description="Due date")
    payable_on_demand: Optional[bool] = Field(None, description="Payable on demand")
    additional_data: Optional[dict] = Field(None, description="Additional document data")

@router.post("/api/sovereign/endorse/coupon")
def endorse_coupon_endpoint(req: CouponEndorsementRequest):
    """
    Endorses a payment coupon using UCC 3-305 provisions.

    This endpoint processes payment coupons through the sovereign endorsement system,
    applying UCC 3-305 endorsement provisions and embedding trust corpus logic.
    """
    try:
        # Convert request to dictionary
        coupon_data = req.dict()

        # Process endorsement
        result = endorse_coupon(coupon_data)

        if result["success"]:
            return {
                "success": True,
                "message": result["message"],
                "endorsed_coupon": result["endorsed_coupon"]
            }
        else:
            raise HTTPException(status_code=400, detail=result["message"])

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to endorse coupon: {str(e)}")

@router.post("/api/sovereign/endorse/bill")
def endorse_bill_endpoint(req: BillEndorsementRequest):
    """
    Endorses a bill using private trust endorsement strategies.

    This endpoint processes bills through the sovereign endorsement system,
    creating trust corpus embeddings and establishing settlement authority.
    """
    try:
        # Convert request to dictionary
        bill_data = req.dict()

        # Process bill endorsement
        result = endorse_bill(bill_data)

        if result["success"]:
            return {
                "success": True,
                "message": result["message"],
                "endorsed_bill": result["endorsed_bill"]
            }
        else:
            raise HTTPException(status_code=400, detail=result["message"])

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to endorse bill: {str(e)}")

@router.post("/api/sovereign/create/promissory-note")
def create_promissory_note_endpoint(req: PromissoryNoteRequest):
    """
    Creates a promissory note using UCC 3-104 compliance.

    This endpoint generates promissory notes with proper authorship declarations
    and UCC Article 3 compliance for negotiable instruments.
    """
    try:
        # Convert request to dictionary
        note_data = req.dict()

        # Process promissory note creation
        result = create_promissory_note(note_data)

        if result["success"]:
            return {
                "success": True,
                "message": result["message"],
                "promissory_note": result["promissory_note"]
            }
        else:
            raise HTTPException(status_code=400, detail=result["message"])

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create promissory note: {str(e)}")

@router.post("/api/sovereign/validate/negotiability")
def validate_negotiability_endpoint(req: NegotiabilityValidationRequest):
    """
    Validates negotiability of financial instruments under UCC 3-104.

    This endpoint analyzes financial documents to determine if they meet
    UCC 3-104 requirements for negotiable instruments.
    """
    try:
        # Convert request to dictionary
        document_data = req.dict()

        # Process negotiability validation
        result = validate_negotiability(document_data)

        if result["success"]:
            return {
                "success": True,
                "message": result["message"],
                "validation_result": result["validation_result"]
            }
        else:
            raise HTTPException(status_code=400, detail=result["message"])

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to validate negotiability: {str(e)}")

@router.get("/api/sovereign/endorsement/info")
def get_endorsement_info():
    """
    Returns information about available endorsement types and UCC provisions.

    This endpoint provides educational information about the endorsement system,
    UCC provisions, and available sovereign invocation strategies.
    """
    try:
        endorsement_info = {
            "available_endorsement_types": [
                {
                    "type": "private_trust",
                    "description": "Endorses instrument into private trust corpus for settlement",
                    "ucc_provisions": ["UCC 3-305", "UCC 3-302"],
                    "use_case": "Payment coupons, bills, commercial instruments"
                },
                {
                    "type": "acceptance_for_value",
                    "description": "Accepts instrument for value and returns for settlement",
                    "ucc_provisions": ["UCC 3-302"],
                    "use_case": "Government notices, bills, financial instruments"
                }
            ],
            "ucc_provisions": {
                "UCC 3-104": "Defines negotiable instruments and requirements",
                "UCC 3-302": "Covers negotiable instrument requirements and holder rights",
                "UCC 3-305": "Specifies endorsement provisions and types",
                "UCC 3-401": "Defines holder in due course status and protections"
            },
            "semantic_lineage": {
                "description": "Tracks the authorship and jurisdiction of each endorsement",
                "components": ["author", "jurisdiction", "trust_corpus", "ucc_compliance"],
                "purpose": "Establishes clear chain of authority and sovereignty"
            }
        }

        return {
            "success": True,
            "endorsement_info": endorsement_info,
            "message": "Endorsement information retrieved successfully"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve endorsement info: {str(e)}")

@router.get("/api/sovereign/endorsement/templates")
def get_endorsement_templates():
    """
    Returns available endorsement templates and examples.

    This endpoint provides template structures for different types of
    endorsements that can be used as examples or starting points.
    """
    try:
        templates = {
            "coupon_endorsement_template": {
                "endorser_name": "John Doe",
                "amount": "150.00",
                "payee": "XYZ Corporation",
                "account_number": "123456789",
                "endorsement_type": "private_trust",
                "due_date": "2024-12-31"
            },
            "bill_endorsement_template": {
                "endorser_name": "John Doe",
                "amount": "250.00",
                "creditor": "ABC Services",
                "bill_number": "INV-2024-001",
                "endorsement_type": "private_trust"
            },
            "promissory_note_template": {
                "maker_name": "John Doe",
                "amount": "1000.00",
                "payee": "Jane Smith",
                "note_title": "Private Promissory Note",
                "due_date": "2025-12-31",
                "payable_on_demand": False,
                "jurisdiction": "Common Law"
            }
        }

        return {
            "success": True,
            "templates": templates,
            "message": "Endorsement templates retrieved successfully"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve templates: {str(e)}")