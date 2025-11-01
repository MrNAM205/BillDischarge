
from datetime import datetime
import os

def load_template(name):
    path = f"config/endorsement_templates/{name}.txt"
    with open(path, "r") as f:
        return f.read()

def apply_endorsement(bill, template, signer, jurisdiction, private_key):
    template_text = load_template(template)
    filled = template_text.format(**bill)
    signed = {
        "endorsement": filled,
        "signer": signer,
        "jurisdiction": jurisdiction,
        "timestamp": datetime.utcnow().isoformat(),
        "signature": f"Signed with key {private_key[:6]}…"
    }
    return signed

def classify_instrument(bill):
    if "description" in bill and "amount" in bill:
        if "issuer" in bill and "recipient" in bill:
            return "draft"  # Most utility bills are orders to pay
    return "note"

def prepare_endorsement_for_signing(bill_data: dict, endorsement_text: str) -> dict: # Added
    return {
        "document_type": bill_data.get("document_type", "Unknown"),
        "bill_number": bill_data.get("bill_number", "N/A"),
        "customer_name": bill_data.get("customer_name", "N/A"),
        "total_amount": bill_data.get("total_amount", "N/A"),
        "currency": bill_data.get("currency", "N/A"),
        "endorsement_date": datetime.now().strftime("%Y-%m-%d"),
        "endorser_id": "WEB-UTIL-001",
        "endorsement_text": endorsement_text
    }
