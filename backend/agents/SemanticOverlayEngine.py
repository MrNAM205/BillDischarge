import re

TRAPS = {
  "citizen": "Presumes federal jurisdiction under 8 USC §1401.",
  "resident": "Implies domicile and commercial liability.",
  "liable": "Triggers presumption of debt or obligation.",
  "person": "May refer to legal fiction under 1 USC §8.",
  "individual": "Often used to mask corporate or trust overlays."
}

def scan_content(content):
  flags = []
  for term, message in TRAPS.items():
    if re.search(rf"\b{term}\b", content, re.IGNORECASE):
      flags.append({ "term": term, "message": message })
  return flags