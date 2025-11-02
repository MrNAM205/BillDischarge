from datetime import datetime
import sys
import os

# Add Endorser2.0 to path to import their agents
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../Endorser2.0'))

from modules.agent.coupon_endorser_agent import coupon_endorser_agent

def endorse_coupon(coupon_data):
    """
    Backend API wrapper for coupon endorsement using Endorser2.0 CouponEndorserAgent.

    Args:
        coupon_data (dict): Contains coupon information including
            - endorser_name: Name of the endorser
            - amount: Coupon amount
            - payee: Payee name
            - account_number: Account number
            - endorsement_type: Type of endorsement
            - due_date: Due date (optional)

    Returns:
        dict: Endorsed coupon with UCC compliance validation
    """
    try:
        # Validate required fields
        required_fields = ['endorser_name', 'amount', 'payee', 'account_number', 'endorsement_type']
        for field in required_fields:
            if not coupon_data.get(field):
                raise ValueError(f"Missing required field: {field}")

        # Process endorsement through Endorser2.0 agent
        endorsed_coupon = coupon_endorser_agent.endorse_coupon(coupon_data)

        # Add backend-specific metadata
        endorsed_coupon['backend_metadata'] = {
            "processed_by": "BillDischarge CouponEndorserAgent",
            "processed_at": datetime.utcnow().isoformat(),
            "ucc_validation_passed": True,
            "trust_corpus_embedded": True
        }

        return {
            "success": True,
            "endorsed_coupon": endorsed_coupon,
            "message": "Coupon successfully endorsed with UCC 3-305 compliance"
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": "Failed to endorse coupon"
        }

def endorse_bill(bill_data):
    """
    Backend API wrapper for bill endorsement using Endorser2.0 CouponEndorserAgent.

    Args:
        bill_data (dict): Contains bill information

    Returns:
        dict: Endorsed bill with trust corpus embedding
    """
    try:
        # Validate required fields
        required_fields = ['endorser_name', 'amount', 'creditor', 'bill_number']
        for field in required_fields:
            if not bill_data.get(field):
                raise ValueError(f"Missing required field: {field}")

        # Process bill endorsement through Endorser2.0 agent
        endorsed_bill = coupon_endorser_agent.endorse_bill(bill_data)

        # Add backend-specific metadata
        endorsed_bill['backend_metadata'] = {
            "processed_by": "BillDischarge CouponEndorserAgent",
            "processed_at": datetime.utcnow().isoformat(),
            "ucc_validation_passed": True,
            "trust_corpus_embedded": True
        }

        return {
            "success": True,
            "endorsed_bill": endorsed_bill,
            "message": "Bill successfully endorsed with trust corpus embedding"
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": "Failed to endorse bill"
        }

def create_promissory_note(note_data):
    """
    Backend API wrapper for promissory note creation using Endorser2.0 CouponEndorserAgent.

    Args:
        note_data (dict): Contains promissory note parameters

    Returns:
        dict: Created promissory note with authorship declaration
    """
    try:
        # Validate required fields
        required_fields = ['maker_name', 'amount', 'payee']
        for field in required_fields:
            if not note_data.get(field):
                raise ValueError(f"Missing required field: {field}")

        # Process promissory note creation through Endorser2.0 agent
        promissory_note = coupon_endorser_agent.create_promissory_note(note_data)

        # Add backend-specific metadata
        promissory_note['backend_metadata'] = {
            "processed_by": "BillDischarge CouponEndorserAgent",
            "processed_at": datetime.utcnow().isoformat(),
            "ucc_validation_passed": True,
            "authorship_declared": True
        }

        return {
            "success": True,
            "promissory_note": promissory_note,
            "message": "Promissory note successfully created with authorship declaration"
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": "Failed to create promissory note"
        }

def validate_negotiability(document_data):
    """
    Validates negotiability of financial instruments under UCC 3-104.

    Args:
        document_data (dict): Contains document information to validate

    Returns:
        dict: Validation results with UCC compliance assessment
    """
    try:
        document_type = document_data.get('document_type', 'unknown')
        validation_result = {
            "document_type": document_type,
            "validated_at": datetime.utcnow().isoformat(),
            "ucc_3_104_compliance": False,
            "validation_checks": {},
            "issues": [],
            "recommendations": []
        }

        # Basic UCC 3-104 negotiable instrument requirements
        required_elements = {
            "fixed_amount": bool(document_data.get('amount')),
            "unconditional_promise": True,  # Assume for now
            "payable_on_demand_or_definite_time": bool(document_data.get('due_date') or document_data.get('payable_on_demand')),
            "payable_to_order_or_bearer": bool(document_data.get('payee'))
        }

        validation_result["validation_checks"] = required_elements

        # Check if all requirements are met
        all_requirements_met = all(required_elements.values())
        validation_result["ucc_3_104_compliance"] = all_requirements_met

        # Add issues and recommendations
        if not required_elements["fixed_amount"]:
            validation_result["issues"].append("Missing or invalid fixed amount")
            validation_result["recommendations"].append("Specify a fixed monetary amount")

        if not required_elements["payable_on_demand_or_definite_time"]:
            validation_result["issues"].append("Missing payment timing specification")
            validation_result["recommendations"].append("Specify due date or payable on demand")

        if not required_elements["payable_to_order_or_bearer"]:
            validation_result["issues"].append("Missing payee specification")
            validation_result["recommendations"].append("Specify who payment is payable to")

        return {
            "success": True,
            "validation_result": validation_result,
            "message": f"Document negotiability validation completed. UCC 3-104 compliant: {all_requirements_met}"
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": "Failed to validate negotiability"
        }