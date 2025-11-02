from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from agents.SemanticWarfareAgent import scan_document, detect_traps, generate_rebuttal, get_common_trap_patterns

router = APIRouter()

class DocumentScanRequest(BaseModel):
    document_text: str = Field(..., description="Text content to scan for semantic warfare")
    scan_type: Optional[str] = Field("comprehensive", description="Type of scan (comprehensive, traps_only, framing_only)")
    custom_parameters: Optional[Dict[str, Any]] = Field(None, description="Custom scan parameters")

class TrapDetectionRequest(BaseModel):
    document_text: str = Field(..., description="Text content to analyze for semantic traps")
    trap_categories: Optional[list] = Field(None, description="Specific trap categories to focus on")
    severity_threshold: Optional[str] = Field("low", description="Minimum severity level (low, medium, high)")

class RebuttalGenerationRequest(BaseModel):
    semantic_analysis: Dict[str, Any] = Field(..., description="Results from semantic analysis")
    custom_parameters: Optional[Dict[str, Any]] = Field(None, description="Custom parameters for rebuttal generation")
    include_signatory_block: Optional[bool] = Field(False, description="Include custom signatory block")
    signatory_name: Optional[str] = Field(None, description="Name for signatory block")
    jurisdiction: Optional[str] = Field("Common Law", description="Jurisdiction for rebuttal")

class SemanticTrapPatternsRequest(BaseModel):
    category_filter: Optional[str] = Field(None, description="Filter by trap category")
    severity_filter: Optional[str] = Field(None, description="Filter by severity level")

@router.post("/api/sovereign/semantic/scan")
def scan_document_endpoint(req: DocumentScanRequest):
    """
    Performs comprehensive semantic warfare analysis on document text.

    This endpoint scans documents for institutional framing, semantic traps,
    and generates detailed analysis with categorization and severity assessment.
    """
    try:
        if not req.document_text or len(req.document_text.strip()) < 10:
            raise HTTPException(status_code=400, detail="Document text must be at least 10 characters")

        # Perform semantic scan
        result = scan_document(req.document_text)

        if result["success"]:
            # Add custom processing based on scan type
            if req.scan_type == "traps_only":
                # Return only trap detection results
                trap_result = detect_traps(req.document_text)
                if trap_result["success"]:
                    result["semantic_analysis"]["institutional_framing"] = {}
                    result["semantic_analysis"]["semantic_traps"] = trap_result["trap_detection"]["trap_analysis"]["semantic_traps"]

            elif req.scan_type == "framing_only":
                # Return only institutional framing results
                result["semantic_analysis"]["semantic_traps"] = []

            # Add custom parameters if provided
            if req.custom_parameters:
                result["semantic_analysis"]["custom_parameters"] = req.custom_parameters

            return {
                "success": True,
                "message": result["message"],
                "semantic_analysis": result["semantic_analysis"]
            }
        else:
            raise HTTPException(status_code=400, detail=result["message"])

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to scan document: {str(e)}")

@router.post("/api/sovereign/semantic/traps")
def detect_traps_endpoint(req: TrapDetectionRequest):
    """
    Detects semantic traps in document text.

    This endpoint focuses specifically on semantic trap detection with
    detailed categorization and severity assessment.
    """
    try:
        if not req.document_text or len(req.document_text.strip()) < 10:
            raise HTTPException(status_code=400, detail="Document text must be at least 10 characters")

        # Perform trap detection
        result = detect_traps(req.document_text)

        if result["success"]:
            trap_detection = result["trap_detection"]

            # Apply category filter if specified
            if req.trap_categories:
                filtered_traps = []
                for trap in trap_detection["trap_analysis"]["semantic_traps"]:
                    if trap.get("trap_category") in req.trap_categories:
                        filtered_traps.append(trap)
                trap_detection["trap_analysis"]["semantic_traps"] = filtered_traps
                trap_detection["trap_statistics"]["total_traps"] = len(filtered_traps)

            # Apply severity filter if specified
            severity_order = {"low": 0, "medium": 1, "high": 2}
            min_severity = severity_order.get(req.severity_threshold, 0)

            filtered_traps = []
            for trap in trap_detection["trap_analysis"]["semantic_traps"]:
                trap_severity = severity_order.get(trap.get("severity", "low"), 0)
                if trap_severity >= min_severity:
                    filtered_traps.append(trap)

            trap_detection["trap_analysis"]["semantic_traps"] = filtered_traps
            trap_detection["trap_statistics"]["total_traps"] = len(filtered_traps)

            return {
                "success": True,
                "message": result["message"],
                "trap_detection": trap_detection
            }
        else:
            raise HTTPException(status_code=400, detail=result["message"])

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to detect semantic traps: {str(e)}")

@router.post("/api/sovereign/semantic/rebuttal")
def generate_rebuttal_endpoint(req: RebuttalGenerationRequest):
    """
    Generates narrative sovereignty rebuttal based on semantic analysis.

    This endpoint creates comprehensive rebuttals to institutional framing
    and semantic traps, establishing narrative sovereignty.
    """
    try:
        if not req.semantic_analysis:
            raise HTTPException(status_code=400, detail="Semantic analysis data is required")

        # Prepare custom parameters
        custom_params = req.custom_parameters or {}
        if req.include_signatory_block:
            custom_params.update({
                "include_signatory_block": True,
                "signatory_name": req.signatory_name or "SOVEREIGN INDIVIDUAL",
                "jurisdiction": req.jurisdiction,
                "capacity": "Principal Author"
            })

        # Generate rebuttal
        result = generate_rebuttal(req.semantic_analysis, custom_params)

        if result["success"]:
            return {
                "success": True,
                "message": result["message"],
                "narrative_rebuttal": result["narrative_rebuttal"]
            }
        else:
            raise HTTPException(status_code=400, detail=result["message"])

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate rebuttal: {str(e)}")

@router.get("/api/sovereign/semantic/traps")
def get_common_trap_patterns_endpoint(category_filter: Optional[str] = None, severity_filter: Optional[str] = None):
    """
    Returns common semantic trap patterns for educational purposes.

    This endpoint provides information about common semantic traps,
    their contexts, and strategies for rebuttal.
    """
    try:
        result = get_common_trap_patterns()

        if result["success"]:
            common_patterns = result["common_patterns"]

            # Apply category filter if specified
            if category_filter and category_filter in common_patterns:
                common_patterns = {category_filter: common_patterns[category_filter]}

            # Apply severity filter (this would need more sophisticated logic in a real implementation)
            if severity_filter:
                # For now, just return all patterns
                pass

            return {
                "success": True,
                "message": result["message"],
                "common_patterns": common_patterns,
                "filter_applied": {
                    "category": category_filter,
                    "severity": severity_filter
                }
            }
        else:
            raise HTTPException(status_code=400, detail=result["message"])

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve trap patterns: {str(e)}")

@router.get("/api/sovereign/semantic/analysis-info")
def get_semantic_analysis_info():
    """
    Returns information about semantic warfare analysis capabilities.

    This endpoint provides educational information about semantic warfare,
    institutional framing, and the analysis process.
    """
    try:
        analysis_info = {
            "semantic_warfare_overview": {
                "description": "Analysis of how language is used to create presumptions and impose obligations",
                "key_concepts": [
                    "Institutional framing",
                    "Semantic traps",
                    "Adhesion contracts",
                    "Presumption of consent",
                    "Narrative sovereignty"
                ]
            },
            "analysis_types": {
                "comprehensive": "Full analysis including institutional framing and semantic traps",
                "traps_only": "Focus specifically on semantic trap detection",
                "framing_only": "Focus on institutional framing analysis"
            },
            "trap_categories": {
                "identity_framing": "Legal fiction identity constructs (person, citizen, resident)",
                "obligation_imposition": "Language imposing obligations without consent",
                "jurisdiction_presumption": "Presumptions about government jurisdiction",
                "consent_presumption": "Implied consent through adhesion contracts"
            },
            "severity_levels": {
                "high": "Directly impacts rights and creates significant obligations",
                "medium": "Creates presumptions that may lead to obligations",
                "low": "Subtle framing that may support other presumptions"
            },
            "rebuttal_strategies": {
                "direct_rebuttal": "Explicitly reject the presumption or framing",
                "affirmative_declaration": "Declare correct status or jurisdiction",
                "conditional_acceptance": "Accept under specific conditions",
                "narrative_sovereignty": "Reclaim control over narrative and definitions"
            }
        }

        return {
            "success": True,
            "analysis_info": analysis_info,
            "message": "Semantic analysis information retrieved successfully"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve analysis info: {str(e)}")

@router.post("/api/sovereign/semantic/batch-analyze")
def batch_analyze_documents_endpoint(documents: list[DocumentScanRequest]):
    """
    Performs semantic analysis on multiple documents.

    This endpoint processes multiple documents in a single request,
    providing comparative analysis across documents.
    """
    try:
        if not documents or len(documents) > 10:
            raise HTTPException(status_code=400, detail="Provide 1-10 documents for batch analysis")

        results = []
        comparative_analysis = {
            "total_documents": len(documents),
            "total_framing_detected": 0,
            "total_traps_detected": 0,
            "most_common_traps": {},
            "highest_risk_document": None,
            "risk_distribution": {"high": 0, "medium": 0, "low": 0}
        }

        all_traps = []

        for i, doc_request in enumerate(documents):
            try:
                # Analyze each document
                result = scan_document(doc_request.document_text)

                if result["success"]:
                    doc_result = {
                        "document_index": i,
                        "semantic_analysis": result["semantic_analysis"]
                    }
                    results.append(doc_result)

                    # Collect data for comparative analysis
                    analysis = result["semantic_analysis"]
                    framing_count = analysis.get("institutional_framing", {}).get("total_framing_detected", 0)
                    trap_count = analysis.get("semantic_traps", {}).get("total_traps_detected", 0)
                    risk_level = analysis.get("semantic_traps", {}).get("document_classification", "low")

                    comparative_analysis["total_framing_detected"] += framing_count
                    comparative_analysis["total_traps_detected"] += trap_count
                    comparative_analysis["risk_distribution"][risk_level] = comparative_analysis["risk_distribution"].get(risk_level, 0) + 1

                    # Collect all traps for most common analysis
                    traps = analysis.get("semantic_traps", {}).get("semantic_traps", [])
                    all_traps.extend(traps)

                    # Track highest risk document
                    if risk_level == "high":
                        comparative_analysis["highest_risk_document"] = i

                else:
                    results.append({
                        "document_index": i,
                        "error": result["message"]
                    })

            except Exception as e:
                results.append({
                    "document_index": i,
                    "error": str(e)
                })

        # Calculate most common traps
        trap_counts = {}
        for trap in all_traps:
            trap_type = trap.get("trap_type", "unknown")
            trap_counts[trap_type] = trap_counts.get(trap_type, 0) + 1

        comparative_analysis["most_common_traps"] = sorted(trap_counts.items(), key=lambda x: x[1], reverse=True)[:5]

        return {
            "success": True,
            "message": f"Batch analysis completed for {len(documents)} documents",
            "results": results,
            "comparative_analysis": comparative_analysis
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to perform batch analysis: {str(e)}")