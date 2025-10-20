import time
import re
from functools import wraps

def time_function(f):
    """A decorator to profile function execution time."""
    @wraps(f)
    def wrapper(*args, **kwargs):
        print(f"PROFILING: Running {f.__name__}...")
        start_time = time.time()
        result = f(*args, **kwargs)
        end_time = time.time()
        print(f"PROFILING: {f.__name__} finished in {end_time - start_time:.4f}s")
        return result
    return wrapper

class InstrumentAnnotator:
    """
    A class to annotate financial instruments, profile performance, and detect contradictions.
    """
    def __init__(self):
        print("InstrumentAnnotator initialized. Ready for analysis.")
        self.contradiction_keywords = ["VOID", "FRAUD", "PROTEST", "ALL RIGHTS RESERVED"]

    @time_function
    def _parse_structured_bill(self, text):
        """Parses a structured bill to extract key metadata."""
        metadata = {
            "to": None,
            "from": None,
            "amount_due": None
        }
        
        to_match = re.search(r"^TO:\s*(.*)", text, re.MULTILINE)
        if to_match:
            metadata["to"] = to_match.group(1).strip()

        from_match = re.search(r"^FROM:\s*(.*)", text, re.MULTILINE)
        if from_match:
            metadata["from"] = from_match.group(1).strip()
            
        amount_match = re.search(r"^AMOUNT DUE:\s*(.*)", text, re.MULTILINE)
        if amount_match:
            metadata["amount_due"] = amount_match.group(1).strip()
            
        return metadata

    @time_function
    def _check_contradictions(self, text):
        """Scans text for keywords that indicate a contradiction."""
        found_contradictions = []
        for keyword in self.contradiction_keywords:
            if re.search(keyword, text, re.IGNORECASE):
                found_contradictions.append(keyword)
        return found_contradictions

    def annotate(self, instrument_text):
        """
        Performs a full analysis of the instrument text, including parsing and contradiction scanning.
        """
        print("\n--- Starting Instrument Annotation ---")
        metadata = self._parse_structured_bill(instrument_text)
        contradictions = self._check_contradictions(instrument_text)
        print("--- Annotation Complete ---")
        
        return {
            "metadata": metadata,
            "contradictions": contradictions,
            "profiling_summary": "See console output for detailed profiling."
        }

