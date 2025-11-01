import re
from datetime import datetime

TRAPS = {
  "citizen": "Presumes federal jurisdiction under 8 USC §1401.",
  "resident": "Implies domicile and commercial liability.",
  "liable": "Triggers presumption of debt or obligation.",
  "person": "May refer to legal fiction under 1 USC §8.",
  "individual": "Often used to mask corporate overlays."
}

REBUTTALS = {
  "citizen": "Rebutted presumption of federal citizenship.",
  "resident": "Rebutted domicile and liability presumption.",
  "liable": "Rebutted debt presumption.",
  "person": "Rebutted legal fiction presumption.",
  "individual": "Rebutted corporate overlay presumption."
}

def audit_semantics(content):
  report = {
    "timestamp": datetime.utcnow().isoformat(),
    "traps_detected": [],
    "rebuttals_injected": [],
    "jurisdictional_overlay": "Common Law / Divine Law"
  }

  for term, trap in TRAPS.items():
    if re.search(rf"\b{term}\b", content, re.IGNORECASE):
      report["traps_detected"].append({ "term": term, "trap": trap })
      if REBUTTALS[term] in content:
        report["rebuttals_injected"].append({ "term": term, "rebuttal": REBUTTALS[term] })

  return report