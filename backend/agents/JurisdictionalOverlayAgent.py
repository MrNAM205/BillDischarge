from datetime import datetime

REBUTTAL_MAP = {
    "title42": "I rebut the presumption of maritime jurisdiction under Title 42.",
    "ucc": "I rebut the presumption of commercial jurisdiction under the Uniform Commercial Code."
}

def create_overlay(venue, rebuttals):
  overlay = {
    "timestamp": datetime.utcnow().isoformat(),
    "source_logic": "David Straight — Jurisdictional Navigation",
    "jurisdictional_overlay": {
      "venue": venue,
      "rebuttals": [REBUTTAL_MAP[r] for r in rebuttals if r in REBUTTAL_MAP],
      "protections_invoked": [
          "Article IV, Section 2 (Privileges and Immunities)",
          "Bill of Rights (Amendments 1-10)"
      ]
    }
  }
  return overlay