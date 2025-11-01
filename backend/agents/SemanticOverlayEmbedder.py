import re

REBUTTALS = {
  "citizen": "I rebut the presumption of federal citizenship under 8 USC §1401.",
  "resident": "I rebut the presumption of domicile and commercial liability.",
  "liable": "I rebut any presumption of debt or obligation.",
  "person": "I rebut the presumption that I am a legal fiction under 1 USC §8.",
  "individual": "I rebut the use of corporate overlays to describe my living status."
}

def embed_rebuttals(content):
  embedded = content
  for term, rebuttal in REBUTTALS.items():
    pattern = rf"\b{term}\b"
    if re.search(pattern, embedded, re.IGNORECASE):
      embedded += f"\n\n[Semantic Rebuttal: {term}] {rebuttal}"
  return embedded
