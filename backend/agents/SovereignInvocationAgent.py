from datetime import datetime
from agents.CognitiveOverlayAgent import scan_and_inject as scan_cognitive
from agents.StatusDeclarationAgent import create_declaration
from agents.JurisdictionalOverlayAgent import create_overlay

def create_sovereign_manifest(content, fullName, birthState, signer, jurisdiction, venue, rebuttals):
    cognitive_overlay = scan_cognitive(content)
    status_declaration = create_declaration(fullName, birthState, signer, jurisdiction, privateKey="dummy_key_for_now") # Note: private key handling needs to be improved
    jurisdictional_overlay = create_overlay(venue, rebuttals)

    manifest = {
        "sovereign_invocation_manifest": {
            "timestamp": datetime.utcnow().isoformat(),
            "overlays": {
                "cognitive_overlay": cognitive_overlay,
                "status_declaration": status_declaration,
                "jurisdictional_overlay": jurisdictional_overlay,
            },
            "signer": signer,
            "jurisdiction": jurisdiction,
            "ready_for_signing": True
        }
    }
    return manifest