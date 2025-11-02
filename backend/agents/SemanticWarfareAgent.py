from datetime import datetime
import sys
import os

# Add Endorser2.0 to path to import their agents
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../Endorser2.0'))

from modules.agent.semantic_warfare_agent import semantic_warfare_agent

def scan_document(document_text):
    """
    Backend API wrapper for document semantic scanning using Endorser2.0 SemanticWarfareAgent.

    Args:
        document_text (str): Text content to scan for semantic traps

    Returns:
        dict: Complete semantic analysis with institutional framing detection
    """
    try:
        if not document_text or not document_text.strip():
            raise ValueError("Document text cannot be empty")

        # Perform institutional framing analysis
        framing_analysis = semantic_warfare_agent.scan_institutional_framing(document_text)

        # Perform semantic trap detection
        trap_analysis = semantic_warfare_agent.detect_semantic_traps(document_text)

        # Combine analyses for comprehensive result
        complete_analysis = {
            "document_analysis": {
                "document_length": len(document_text),
                "analyzed_at": datetime.utcnow().isoformat(),
                "analysis_type": "comprehensive_semantic_warfare"
            },
            "institutional_framing": framing_analysis,
            "semantic_traps": trap_analysis,
            "summary": {
                "total_framing_detected": len(framing_analysis.get("institutional_framing", [])),
                "total_traps_detected": len(trap_analysis.get("semantic_traps", [])),
                "document_risk_level": trap_analysis.get("document_classification", "unknown"),
                "high_severity_items": _count_high_severity_items(framing_analysis, trap_analysis)
            }
        }

        return {
            "success": True,
            "semantic_analysis": complete_analysis,
            "message": "Document semantic scan completed successfully"
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": "Failed to scan document for semantic warfare"
        }

def detect_traps(document_text):
    """
    Backend API wrapper for semantic trap detection.

    Args:
        document_text (str): Text content to analyze

    Returns:
        dict: Semantic trap detection results
    """
    try:
        if not document_text or not document_text.strip():
            raise ValueError("Document text cannot be empty")

        # Perform semantic trap detection
        trap_analysis = semantic_warfare_agent.detect_semantic_traps(document_text)

        # Add backend-specific processing
        semantic_traps = trap_analysis.get("semantic_traps", [])

        # Categorize traps by severity and type
        categorized_traps = {
            "high_severity": [trap for trap in semantic_traps if trap.get("severity") == "high"],
            "medium_severity": [trap for trap in semantic_traps if trap.get("severity") == "medium"],
            "low_severity": [trap for trap in semantic_traps if trap.get("severity") == "low"],
            "by_category": {}
        }

        # Group traps by category
        for trap in semantic_traps:
            category = trap.get("trap_category", "other")
            if category not in categorized_traps["by_category"]:
                categorized_traps["by_category"][category] = []
            categorized_traps["by_category"][category].append(trap)

        trap_result = {
            "trap_analysis": trap_analysis,
            "categorized_traps": categorized_traps,
            "trap_statistics": {
                "total_traps": len(semantic_traps),
                "unique_trap_types": len(set(trap.get("trap_type") for trap in semantic_traps)),
                "high_risk_count": len(categorized_traps["high_severity"]),
                "most_common_trap": _find_most_common_trap(semantic_traps)
            }
        }

        return {
            "success": True,
            "trap_detection": trap_result,
            "message": f"Semantic trap detection completed. Found {len(semantic_traps)} traps"
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": "Failed to detect semantic traps"
        }

def generate_rebuttal(semantic_analysis, custom_parameters=None):
    """
    Backend API wrapper for narrative sovereignty rebuttal generation.

    Args:
        semantic_analysis (dict): Results from semantic analysis
        custom_parameters (dict): Optional custom parameters for rebuttal

    Returns:
        dict: Generated narrative sovereignty rebuttal
    """
    try:
        if not semantic_analysis:
            raise ValueError("Semantic analysis data is required")

        # Extract semantic traps and institutional framing
        semantic_traps = semantic_analysis.get("semantic_traps", [])
        institutional_framing = semantic_analysis.get("institutional_framing", [])

        # Prepare analysis data for Endorser2.0 agent
        analysis_data = {
            "semantic_traps": semantic_traps,
            "institutional_framing": institutional_framing
        }

        # Generate rebuttal using Endorser2.0 agent
        rebuttal = semantic_warfare_agent.generate_narrative_rebuttal(analysis_data)

        # Add backend-specific metadata and customization
        if custom_parameters:
            rebuttal["custom_parameters"] = custom_parameters
            if custom_parameters.get("include_signatory_block"):
                rebuttal["signatory_block"] = _generate_signatory_block(custom_parameters)

        rebuttal["backend_metadata"] = {
            "generated_by": "BillDischarge SemanticWarfareAgent",
            "generated_at": datetime.utcnow().isoformat(),
            "based_on_analysis": len(semantic_traps) > 0 or len(institutional_framing) > 0,
            "rebuttal_strength": _assess_rebuttal_strength(semantic_traps, institutional_framing)
        }

        return {
            "success": True,
            "narrative_rebuttal": rebuttal,
            "message": "Narrative sovereignty rebuttal generated successfully"
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": "Failed to generate narrative sovereignty rebuttal"
        }

def get_common_trap_patterns():
    """
    Returns common semantic trap patterns for educational purposes.

    Returns:
        dict: Common trap patterns with explanations and rebuttals
    """
    try:
        # This would come from the Endorser2.0 agent's pattern definitions
        common_patterns = {
            "identity_framing": {
                "traps": ["person", "citizen", "resident"],
                "description": "Institutional constructs that create legal fiction identity",
                "common_contexts": ["government forms", "legal documents", "financial applications"],
                "rebuttal_strategy": "Declare living man/woman status and state national jurisdiction"
            },
            "obligation_imposition": {
                "traps": ["liable", "responsible", "must", "required"],
                "description": "Language that imposes obligations without consent",
                "common_contexts": ["tax notices", "regulatory compliance", "legal demands"],
                "rebuttal_strategy": "Rebut presumptions and require proof of consent"
            },
            "jurisdiction_presumption": {
                "traps": ["subject to", "jurisdiction", "authority"],
                "description": "Presumption of government jurisdiction over sovereign individuals",
                "common_contexts": ["court documents", "administrative notices", "legal proceedings"],
                "rebuttal_strategy": "Declare proper jurisdiction and challenge authority"
            },
            "consent_presumption": {
                "traps": ["by using", "you agree", "acceptance of"],
                "description": "Implied consent through adhesion contracts",
                "common_contexts": ["terms of service", "software agreements", "regulatory filings"],
                "rebuttal_strategy": "Explicitly rebut all implied consent and adhesion contracts"
            }
        }

        return {
            "success": True,
            "common_patterns": common_patterns,
            "message": "Common semantic trap patterns retrieved successfully"
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": "Failed to retrieve common trap patterns"
        }

# Helper functions
def _count_high_severity_items(framing_analysis, trap_analysis):
    """Counts high severity semantic warfare items."""
    high_severity_count = 0

    # Count high severity framing
    for framing in framing_analysis.get("institutional_framing", []):
        if framing.get("severity") == "high":
            high_severity_count += 1

    # Count high severity traps
    for trap in trap_analysis.get("semantic_traps", []):
        if trap.get("severity") == "high":
            high_severity_count += 1

    return high_severity_count

def _find_most_common_trap(semantic_traps):
    """Finds the most common trap type."""
    if not semantic_traps:
        return None

    trap_counts = {}
    for trap in semantic_traps:
        trap_type = trap.get("trap_type", "unknown")
        trap_counts[trap_type] = trap_counts.get(trap_type, 0) + 1

    most_common = max(trap_counts.items(), key=lambda x: x[1])
    return {
        "trap_type": most_common[0],
        "count": most_common[1]
    }

def _assess_rebuttal_strength(semantic_traps, institutional_framing):
    """Assesses the strength of rebuttal needed."""
    total_items = len(semantic_traps) + len(institutional_framing)
    high_severity_items = sum(1 for item in semantic_traps + institutional_framing
                             if item.get("severity") == "high")

    if high_severity_items >= 3:
        return "strong_rebuttal_required"
    elif total_items >= 5:
        return "moderate_rebuttal_required"
    elif total_items >= 1:
        return "basic_rebuttal_sufficient"
    else:
        return "minimal_rebuttal_needed"

def _generate_signatory_block(custom_parameters):
    """Generates a custom signatory block."""
    return {
        "signatory_name": custom_parameters.get("signatory_name", "SOVEREIGN INDIVIDUAL"),
        "capacity": custom_parameters.get("capacity", "Principal Author"),
        "jurisdiction": custom_parameters.get("jurisdiction", "Common Law"),
        "reservation": "WITHOUT PREJUDICE UCC 1-207",
        "rights_reserved": "All Rights Reserved"
    }