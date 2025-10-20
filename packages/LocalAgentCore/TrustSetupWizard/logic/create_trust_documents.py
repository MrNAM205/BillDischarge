from datetime import date
import os
from packages.LocalAgentCore.RemedyCompiler.logic.compile import compile_remedy
from packages.LocalAgentCore.remedy_logger import RemedyLogger
from packages.LocalAgentCore.remedy_log import RemedyLog
import datetime

remedy_logger = RemedyLogger()

def create_trust_documents(trust_type, settlor_name, trustee_name, beneficiaries, trust_property):
    """
    Creates the trust documents for a given trust type using compile_remedy.
    """
    today = date.today()

    # We'll create a dummy 'bill' dictionary to pass the data to compile_remedy
    bill = {
        "full_name": settlor_name,
        "birth_location": "Unknown",  # This information might not be relevant for trust documents
        "nationality": "Unknown", # This information might not be relevant for trust documents
        "trust_type": trust_type,
        "trustee_name": trustee_name,
        "beneficiaries": beneficiaries,
        "trust_property": trust_property,
        "date": today.strftime("%B %d, %Y")
    }

    # Call compile_remedy to generate the trust agreement and declaration of trust
    remedy_package = compile_remedy(
        full_name=settlor_name,
        birth_location="Unknown", # This information might not be relevant for trust documents
        nationality="Unknown",  # This information might not be relevant for trust documents
        trust_type=trust_type,
        trustee_name=trustee_name,
        beneficiaries=beneficiaries,
        trust_property=trust_property
    )
    
    trust_agreement = remedy_package.get("cover_letter", "")  # Assuming cover_letter is repurposed for trust agreement
    declaration_of_trust = remedy_package.get("endorsement", "")  # Assuming endorsement is repurposed for declaration of trust

    remedy_logger.log("INFO", f"Generated trust documents for settlor: {settlor_name}")

    # Log the remedy process
    remedy_log = RemedyLog(
        timestamp=datetime.datetime.now(),
        user_id="unknown",  # Replace with actual user ID if available
        module="TrustSetupWizard",
        instrument_ids=[],  # Add relevant instrument IDs if available
        workflow_id=None,  # You might need to determine how to get the workflow ID
        data=bill,
        message=f"Trust documents created for settlor: {settlor_name}",
    )
    remedy_logger.log_remedy(remedy_log)

    return {
        "trust_agreement": trust_agreement,
        "declaration_of_trust": declaration_of_trust
    }
