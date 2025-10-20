from fastapi import FastAPI
from fastapi.responses import FileResponse
from pathlib import Path

from backend.config.config import Config
from backend.routes import (
    annotator,
    discharge,
    document_routes,
    endorsement,
    generator_routes,
    hello,
    nationality,
    packet,
    remedy,
    status,
    logs,
)

config = Config()

app = FastAPI(
    title="Sovereign Financial Cockpit API",
    description="API for managing sovereign financial instruments and processes",
    version="0.1.0",
)

# Define the path to GEMINI.md relative to this file
# This ensures it works regardless of where the app is launched from
GEMINI_MD_PATH = Path(__file__).parent.parent / "GEMINI.md"

# Core routes
app.include_router(hello.router)
app.include_router(annotator.router)
app.include_router(discharge.router)
app.include_router(document_routes.router)
app.include_router(endorsement.router)
app.include_router(generator_routes.router)
app.include_router(nationality.router)
app.include_router(packet.router)
app.include_router(remedy.router)
app.include_router(status.router)
app.include_router(logs.router)


@app.get("/")
async def root():
    return {"message": "Omni2 is online and sovereign."}

@app.get("/gemini", response_class=FileResponse)
async def get_gemini_cognition():
    """Returns the Omni2 cognition framing from GEMINI.md."""
    return str(GEMINI_MD_PATH)
