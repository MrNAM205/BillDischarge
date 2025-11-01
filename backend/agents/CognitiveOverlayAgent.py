import re

NARRATIVE_TRAPS = {
  "compliance": "Suggests submission to institutional authority.",
  "misinformation": "Frames speech as a threat to be managed.",
  "extremism": "Marginalizes dissent as a dangerous outlier."
}

def scan_and_inject(content):
  overlay = {
    "detected_frames": [],
    "counter_clauses": [],
    "source_logic": "Carl Miller — Narrative Sovereignty"
  }
  for term, message in NARRATIVE_TRAPS.items():
    if re.search(rf"\b{term}\b", content, re.IGNORECASE):
      overlay["detected_frames"].append({ "term": term, "message": message })
      overlay["counter_clauses"].append(f"I rebut the presumption that my speech is subject to institutional framing regarding '{term}'.")
  return overlay