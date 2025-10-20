from packages.LocalAgentCore.InstrumentAnnotator.annotator import InstrumentAnnotator
import json

SAMPLE_BILL = '''
TO: JOHN DOE
123 MAIN STREET, ANYTOWN, USA

FROM: MEGA CORP
456 FINANCE BLVD, SUITE 100
FINANCE CITY, USA

DATE: 2025-10-15
INVOICE #: 12345
AMOUNT DUE: $100.00

NOTICE: This is a demand for payment. Failure to remit payment will result in further action.
This instrument is a presentment from a corporation and may be VOID against a sovereign.
Without prejudice, All Rights Reserved.
'''

if __name__ == "__main__":
    print("--- Booting Annotator Demo ---")
    annotator = InstrumentAnnotator()
    
    annotation_result = annotator.annotate(SAMPLE_BILL)
    
    print("\n--- Annotator Result ---")
    print(json.dumps(annotation_result, indent=2))
    print("--- Demo Complete ---")
