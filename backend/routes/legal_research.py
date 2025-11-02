from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
import sys
import os

# Add Endorser2.0 to path to import their agents
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../Endorser2.0'))

from modules.law.law_gathering_engine import law_gathering_engine

router = APIRouter()

class LegalSearchRequest(BaseModel):
    query: str = Field(..., description="Search query for legal authorities")
    jurisdiction: Optional[str] = Field(None, description="Filter by jurisdiction (federal, state, common_law)")
    remedy_type: Optional[str] = Field(None, description="Filter by remedy type (sovereignty, jurisdiction, rights)")
    authority_type: Optional[str] = Field(None, description="Filter by authority type (case_law, statutes, constitutional)")
    max_results: Optional[int] = Field(20, description="Maximum number of results to return")

class CaseLawSearchRequest(BaseModel):
    query: str = Field(..., description="Search query for case law")
    jurisdiction: Optional[str] = Field(None, description="Filter by jurisdiction")
    remedy_type: Optional[str] = Field(None, description="Filter by remedy type")
    time_period: Optional[str] = Field(None, description="Filter by time period (e.g., '1800-1900', '1900-2000', '2000-present')")
    max_results: Optional[int] = Field(10, description="Maximum number of results")

class StatuteSearchRequest(BaseModel):
    query: str = Field(..., description="Search query for statutes")
    code_type: Optional[str] = Field(None, description="Filter by code type (UCC, USC, Constitution, State)")
    jurisdiction: Optional[str] = Field(None, description="Filter by jurisdiction")
    max_results: Optional[int] = Field(10, description="Maximum number of results")

class AffidavitTemplateRequest(BaseModel):
    affidavit_type: Optional[str] = Field(None, description="Filter by affidavit type")
    jurisdiction: Optional[str] = Field(None, description="Filter by jurisdiction")
    use_case: Optional[str] = Field(None, description="Filter by use case")

@router.post("/api/sovereign/legal/search")
def search_legal_authorities_endpoint(req: LegalSearchRequest):
    """
    Performs comprehensive search across legal authorities.

    This endpoint searches case law, constitutional provisions, and remedy statutes
    to provide comprehensive legal authority research for sovereign invocation.
    """
    try:
        if not req.query or len(req.query.strip()) < 3:
            raise HTTPException(status_code=400, detail="Search query must be at least 3 characters")

        # Perform comprehensive legal search
        search_results = law_gathering_engine.search_legal_authorities(req.query)

        # Apply filters if specified
        if req.jurisdiction:
            search_results["case_law"] = [
                case for case in search_results["case_law"]
                if case.get("jurisdiction") == req.jurisdiction
            ]

        if req.remedy_type:
            search_results["case_law"] = [
                case for case in search_results["case_law"]
                if req.remedy_type in case.get("remedy_types", [])
            ]

        if req.authority_type:
            if req.authority_type == "case_law":
                search_results["statutes"] = []
                search_results["constitutional"] = []
            elif req.authority_type == "statutes":
                search_results["case_law"] = []
                search_results["constitutional"] = []
            elif req.authority_type == "constitutional":
                search_results["case_law"] = []
                search_results["statutes"] = []

        # Limit results if specified
        if req.max_results:
            search_results["case_law"] = search_results["case_law"][:req.max_results]
            search_results["statutes"] = search_results["statutes"][:req.max_results]
            search_results["constitutional"] = search_results["constitutional"][:req.max_results]

        # Re-generate summary with filtered results
        total_case_law = len(search_results["case_law"])
        total_statutes = len(search_results["statutes"])
        total_constitutional = len(search_results["constitutional"])

        summary_parts = []
        if total_case_law > 0:
            summary_parts.append(f"Found {total_case_law} relevant case law authorities")
        if total_statutes > 0:
            summary_parts.append(f"Found {total_statutes} relevant statutes and codes")
        if total_constitutional > 0:
            summary_parts.append(f"Found {total_constitutional} constitutional provisions")

        search_results["summary"] = ". ".join(summary_parts) if summary_parts else "No matches found with specified filters."
        search_results["filters_applied"] = {
            "jurisdiction": req.jurisdiction,
            "remedy_type": req.remedy_type,
            "authority_type": req.authority_type,
            "max_results": req.max_results
        }

        return {
            "success": True,
            "message": f"Legal search completed for query: {req.query}",
            "search_results": search_results
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to search legal authorities: {str(e)}")

@router.post("/api/sovereign/legal/cases")
def search_case_law_endpoint(req: CaseLawSearchRequest):
    """
    Searches specifically for case law authorities.

    This endpoint focuses on case law research with detailed filtering options
    for jurisdiction, remedy type, and time period.
    """
    try:
        if not req.query or len(req.query.strip()) < 3:
            raise HTTPException(status_code=400, detail="Search query must be at least 3 characters")

        # Search case law
        case_law_results = law_gathering_engine.search_case_law(
            query=req.query,
            jurisdiction=req.jurisdiction,
            remedy_type=req.remedy_type
        )

        # Apply time period filter if specified
        if req.time_period:
            filtered_cases = []
            for case in case_law_results:
                year = case.get("year", 0)
                if req.time_period == "1800-1900" and 1800 <= year <= 1900:
                    filtered_cases.append(case)
                elif req.time_period == "1900-2000" and 1900 <= year <= 2000:
                    filtered_cases.append(case)
                elif req.time_period == "2000-present" and year >= 2000:
                    filtered_cases.append(case)
            case_law_results = filtered_cases

        # Limit results if specified
        if req.max_results:
            case_law_results = case_law_results[:req.max_results]

        # Generate case-specific analysis
        case_analysis = {
            "total_cases_found": len(case_law_results),
            "time_distribution": {},
            "jurisdiction_distribution": {},
            "remedy_type_distribution": {},
            "most_cited_cases": []
        }

        for case in case_law_results:
            # Analyze time distribution
            decade = (case.get("year", 0) // 10) * 10
            decade_key = f"{decade}s"
            case_analysis["time_distribution"][decade_key] = case_analysis["time_distribution"].get(decade_key, 0) + 1

            # Analyze jurisdiction distribution
            jurisdiction = case.get("jurisdiction", "unknown")
            case_analysis["jurisdiction_distribution"][jurisdiction] = case_analysis["jurisdiction_distribution"].get(jurisdiction, 0) + 1

            # Analyze remedy type distribution
            for remedy_type in case.get("remedy_types", []):
                case_analysis["remedy_type_distribution"][remedy_type] = case_analysis["remedy_type_distribution"].get(remedy_type, 0) + 1

        # Get most cited cases (top 3 by relevance)
        case_analysis["most_cited_cases"] = [
            {
                "case_name": case["case_name"],
                "citation": case["citation"],
                "relevance_score": case["relevance_score"]
            }
            for case in sorted(case_law_results, key=lambda x: x["relevance_score"], reverse=True)[:3]
        ]

        return {
            "success": True,
            "message": f"Case law search completed. Found {len(case_law_results)} cases",
            "case_law_results": case_law_results,
            "case_analysis": case_analysis,
            "search_parameters": {
                "query": req.query,
                "jurisdiction": req.jurisdiction,
                "remedy_type": req.remedy_type,
                "time_period": req.time_period,
                "max_results": req.max_results
            }
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to search case law: {str(e)}")

@router.post("/api/sovereign/legal/statutes")
def search_statutes_endpoint(req: StatuteSearchRequest):
    """
    Searches for remedy statutes and legal codes.

    This endpoint focuses on statutory research including UCC provisions,
    constitutional amendments, and federal/state codes.
    """
    try:
        if not req.query or len(req.query.strip()) < 3:
            raise HTTPException(status_code=400, detail="Search query must be at least 3 characters")

        # Search statutes
        statute_results = law_gathering_engine.find_remedy_statutes(
            query=req.query,
            code_type=req.code_type
        )

        # Apply jurisdiction filter if specified
        if req.jurisdiction:
            # This would need more sophisticated filtering in a real implementation
            pass

        # Limit results if specified
        if req.max_results:
            statute_results = statute_results[:req.max_results]

        # Generate statute analysis
        statute_analysis = {
            "total_statutes_found": len(statute_results),
            "code_type_distribution": {},
            "application_categories": {},
            "key_provisions_summary": []
        }

        for statute in statute_results:
            # Analyze code type distribution
            code_type = statute.get("code_type", "unknown")
            statute_analysis["code_type_distribution"][code_type] = statute_analysis["code_type_distribution"].get(code_type, 0) + 1

            # Analyze application categories
            application = statute.get("application", "")
            if "rights" in application.lower():
                category = "rights_protection"
            elif "commercial" in application.lower() or "negotiable" in application.lower():
                category = "commercial_law"
            elif "government" in application.lower() or "official" in application.lower():
                category = "government_limitation"
            else:
                category = "general"

            statute_analysis["application_categories"][category] = statute_analysis["application_categories"].get(category, 0) + 1

        # Collect key provisions
        for statute in statute_results[:5]:  # Top 5 statutes
            statute_analysis["key_provisions_summary"].append({
                "statute_name": statute["statute_name"],
                "citation": statute["citation"],
                "key_provisions": statute.get("key_provisions", [])
            })

        return {
            "success": True,
            "message": f"Statute search completed. Found {len(statute_results)} statutes",
            "statute_results": statute_results,
            "statute_analysis": statute_analysis,
            "search_parameters": {
                "query": req.query,
                "code_type": req.code_type,
                "jurisdiction": req.jurisdiction,
                "max_results": req.max_results
            }
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to search statutes: {str(e)}")

@router.post("/api/sovereign/legal/affidavits")
def get_affidavit_templates_endpoint(req: AffidavitTemplateRequest):
    """
    Retrieves model affidavit templates for sovereign declarations.

    This endpoint provides template affidavits for various sovereign invocation
    scenarios including status correction, jurisdiction declarations, and rights assertions.
    """
    try:
        # Get model affidavits
        affidavit_results = law_gathering_engine.get_model_affidavits(req.affidavit_type)

        # Apply filters if specified
        if req.jurisdiction:
            affidavit_results = [
                affidavit for affidavit in affidavit_results
                if affidavit.get("jurisdiction", "").lower() == req.jurisdiction.lower()
            ]

        if req.use_case:
            # This would need more sophisticated filtering based on usage notes
            pass

        # Enhance affidavit templates with additional metadata
        enhanced_affidavits = []
        for affidavit in affidavit_results:
            enhanced_affidavit = {
                **affidavit,
                "usage_scenarios": _get_affidavit_usage_scenarios(affidavit.get("type", "")),
                "required_supporting_documents": _get_required_supporting_documents(affidavit.get("type", "")),
                "filing_instructions": _get_filing_instructions(affidavit.get("type", "")),
                "sample_content": _get_sample_content(affidavit.get("type", ""))
            }
            enhanced_affidavits.append(enhanced_affidavit)

        return {
            "success": True,
            "message": f"Retrieved {len(enhanced_affidavits)} affidavit templates",
            "affidavit_templates": enhanced_affidavits,
            "search_parameters": {
                "affidavit_type": req.affidavit_type,
                "jurisdiction": req.jurisdiction,
                "use_case": req.use_case
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve affidavit templates: {str(e)}")

@router.get("/api/sovereign/legal/constitutional")
def get_constitutional_provisions(
    query: Optional[str] = Query(None, description="Search query for constitutional provisions"),
    article: Optional[str] = Query(None, description="Filter by article number"),
    amendment: Optional[str] = Query(None, description="Filter by amendment number")
):
    """
    Retrieves constitutional provisions for sovereign authority research.

    This endpoint provides access to constitutional provisions with
    emphasis on rights protections and government limitations.
    """
    try:
        # Get constitutional provisions from the law gathering engine
        if query:
            search_results = law_gathering_engine.search_legal_authorities(query)
            constitutional_provisions = search_results.get("constitutional", [])
        else:
            # Get all constitutional provisions
            constitutional_provisions = law_gathering_engine.constitutional_corpus

        # Apply filters
        if article:
            constitutional_provisions = [
                provision for provision in constitutional_provisions
                if provision.get("article") == article
            ]

        if amendment:
            constitutional_provisions = [
                provision for provision in constitutional_provisions
                if amendment in provision.get("provision", "").lower()
            ]

        # Group by article for better organization
        grouped_provisions = {}
        for provision in constitutional_provisions:
            article_key = provision.get("article", "Unknown")
            if article_key not in grouped_provisions:
                grouped_provisions[article_key] = []
            grouped_provisions[article_key].append(provision)

        return {
            "success": True,
            "message": f"Retrieved {len(constitutional_provisions)} constitutional provisions",
            "constitutional_provisions": constitutional_provisions,
            "grouped_provisions": grouped_provisions,
            "search_parameters": {
                "query": query,
                "article": article,
                "amendment": amendment
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve constitutional provisions: {str(e)}")

@router.get("/api/sovereign/legal/research-guide")
def get_legal_research_guide():
    """
    Returns guide for legal research in sovereign invocation contexts.

    This endpoint provides educational information about legal research
    methodologies and strategies for sovereign invocation.
    """
    try:
        research_guide = {
            "research_methodology": {
                "primary_sources": [
                    "Constitutional provisions and amendments",
                    "Supreme Court case law",
                    "Federal statutes and codes",
                    "UCC provisions for commercial matters",
                    "State constitutional provisions"
                ],
                "secondary_sources": [
                    "Legal treatises and commentaries",
                    "Law review articles",
                    "Government publications",
                    "Legal dictionaries and encyclopedias"
                ]
            },
            "key_authorities": {
                "sovereignty_cases": [
                    "Hale v. Henkel (201 U.S. 43, 1906)",
                    "Bond v. United States (529 U.S. 334, 2000)",
                    "Murdoch v. Pennsylvania (319 U.S. 105, 1943)"
                ],
                "constitutional_provisions": [
                    "Article IV - Privileges and Immunities",
                    "First Amendment - Religious and Civil Liberties",
                    "Fourth Amendment - Privacy and Security",
                    "Sixth Amendment - Right to Counsel"
                ],
                "statutory_authorities": [
                    "UCC 1-207 - Reservation of Rights",
                    "UCC 3-104 - Negotiable Instruments",
                    "18 USC 241 - Conspiracy Against Rights",
                    "18 USC 242 - Deprivation of Rights Under Color of Law"
                ]
            },
            "research_strategies": {
                "start_broad": "Begin with broad concepts, then narrow to specific authorities",
                "trace_citations": "Follow citation chains to find related authorities",
                "verify_currency": "Ensure authorities are current and good law",
                "cross_reference": "Verify authorities across multiple sources",
                "document_chain": "Maintain clear citation and authority chains"
            },
            "common_research_topics": {
                "sovereign_status": "Research state national vs. U.S. citizen status",
                "jurisdiction_challenges": "Challenge presumptions of federal jurisdiction",
                "rights_assertions": "Assert constitutional and common law rights",
                "commercial_authority": "Establish authority in commercial matters",
                "tax_authority": "Research tax liability and voluntary compliance"
            }
        }

        return {
            "success": True,
            "research_guide": research_guide,
            "message": "Legal research guide retrieved successfully"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve research guide: {str(e)}")

# Helper functions
def _get_affidavit_usage_scenarios(affidavit_type):
    """Returns usage scenarios for affidavit types."""
    scenarios = {
        "status_correction": [
            "Correcting government records",
            "Rebutting presumptions of citizenship",
            "Establishing state national status",
            "Challenging jurisdictional presumptions"
        ],
        "jurisdiction": [
            "Establishing proper venue",
            "Challenging federal jurisdiction",
            "Declaring common law jurisdiction",
            "Contesting administrative jurisdiction"
        ],
        "rights_assertion": [
            "Asserting constitutional rights",
            "Challenging rights violations",
            "Establishing standing to sue",
            "Documenting rights infringements"
        ]
    }
    return scenarios.get(affidavit_type, ["General sovereign declarations"])

def _get_required_supporting_documents(affidavit_type):
    """Returns list of required supporting documents."""
    documents = {
        "status_correction": [
            "Birth certificate",
            "State identification",
            "Witness declarations",
            "Prior government correspondence"
        ],
        "jurisdiction": [
            "Property deeds",
            "Residency documentation",
            "Court filings",
            "Jurisdictional research"
        ],
        "rights_assertion": [
            "Incident documentation",
            "Witness statements",
            "Legal notices received",
            "Rights violation evidence"
        ]
    }
    return documents.get(affidavit_type, ["Supporting documentation as needed"])

def _get_filing_instructions(affidavit_type):
    """Returns filing instructions for affidavits."""
    instructions = {
        "status_correction": "File with county recorder, send via certified mail to relevant agencies",
        "jurisdiction": "File in appropriate court, serve on all interested parties",
        "rights_assertion": "File as evidence in legal proceedings, maintain copies"
    }
    return instructions.get(affidavit_type, "File according to specific legal requirements")

def _get_sample_content(affidavit_type):
    """Returns sample content for affidavit types."""
    samples = {
        "status_correction": "I, [Name], declare under penalty of perjury that I am a state national...",
        "jurisdiction": "I, [Name], declare that this matter falls under common law jurisdiction...",
        "rights_assertion": "I, [Name], declare that my constitutional rights have been violated..."
    }
    return samples.get(affidavit_type, "I, [Name], declare the following facts to be true...")