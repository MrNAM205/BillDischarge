import json
import datetime
from pathlib import Path

router = APIRouter()

# Shared state
last_remedy = {"model": None, "thoughts": None, "fallback": None}

# Prioritized model list
MODEL_PRIORITY = ["gemini-pro", "gemini-flash", "local-autodetect"]

# Create remedy_logs directory if it doesn't exist
LOGS_DIR = Path(__file__).parent.parent.parent / "remedy_logs"
LOGS_DIR.mkdir(exist_ok=True)

class RemedyRequest(BaseModel):
    input: str

def invoke_omni2_cognition(input_text: str, model: str):
    """
    Simulates invoking the Omni2 agent's cognition logic with a specific model.
    This function will randomly simulate a failure for demonstration purposes.
    """
    # Simulate failure for some models
    if model in ["gemini-pro", "gemini-flash"] and random.random() < 0.5:
        raise Exception(f"Model {model} failed to respond.")

    lower_input = input_text.lower()
    
    if any(keyword in lower_input for keyword in ["remedy", "ucc", "discharge"]):
        task_type = "remedy"
    elif "contradiction" in lower_input:
        task_type = "contradiction"
    else:
        task_type = "chat"

    thoughts = f"Task classified as '{task_type}'. Using '{model}' for optimal cognition. Sovereign logic scaffolded."

    if "discharge" in lower_input:
        protocol = """
1. **Notice of Tender of Payment**: Draft a notice of tender of payment to the creditor, citing UCC § 3-603.
2. **Prepare Payment Instrument**: Prepare a payment instrument for the full amount of the obligation.
3. **Send via Certified Mail**: Send the notice and instrument via certified mail with return receipt requested.
4. **Await Response**: If the creditor accepts, the obligation is discharged. If they refuse, they may have waived their claim.
"""
    elif "ucc-3" in lower_input:
        protocol = """
1. **Identify Financing Statement**: Locate the UCC-1 financing statement that needs to be terminated.
2. **Draft UCC-3 Amendment**: Draft a UCC-3 financing statement amendment, checking the "Termination" box.
3. **File with Secretary of State**: File the UCC-3 amendment with the same office where the original UCC-1 was filed.
4. **Confirm Filing**: Obtain a confirmation of filing for your records.
"""
    else:
        protocol = "No specific remedy protocol found for your request. Please be more specific."

    return {
        "protocol": protocol,
        "thoughts": thoughts,
        "model": model
    }

# Optional: Retry limit or timeout
MAX_RETRIES = 3
TIMEOUT = 5  # seconds

@router.post("/api/remedy")
async def scaffold_remedy(request: RemedyRequest = Body(...)):
    """
    Scaffolds a remedy protocol based on a natural language request,
    with a fallback mechanism and logs the transaction.
    """
    response = None
    fallback_annotation = None
    primary_model = MODEL_PRIORITY[0]
    
    for model in MODEL_PRIORITY:
        try:
            response = invoke_omni2_cognition(request.input, model)
            if model != primary_model:
                fallback_annotation = f"Primary model '{primary_model}' failed. Fallback to '{model}' succeeded."
            break
        except Exception as e:
            print(f"Model {model} failed: {e}")
            if model == MODEL_PRIORITY[-1]:
                last_remedy["fallback"] = f"All models failed. Last error: {e}"
                return {"error": "All models failed to respond."}
            continue

    # Log the transaction
    log_data = {
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "request": request.dict(),
        "response": response,
        "fallback": fallback_annotation,
    }
    
    timestamp_str = datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S%f")
    log_file = LOGS_DIR / f"{timestamp_str}.json"
    with open(log_file, "w") as f:
        json.dump(log_data, f, indent=4)

    # Update shared state
    last_remedy["model"] = response["model"]
    last_remedy["thoughts"] = response["thoughts"]
    last_remedy["fallback"] = fallback_annotation
    
    return response
