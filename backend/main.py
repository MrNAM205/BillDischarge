from fastapi import FastAPI
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
)

config = Config()

app = FastAPI(
    title="Sovereign Financial Cockpit API",
    description="API for managing sovereign financial instruments and processes",
    version="0.1.0",
)

# Core routes
app.include_router(hello.router)
app.include_router(annotator.router)
app.include_router(discharge.router)
app.include_router(document_routes.router)
app.include_router(endorsement.router)
app.include_router(generator_routes.router)
app.include_router(nationality.router)
app.include_router(packet.router)


@app.get("/")
async def root():
    return {"message": "Omni2 is online and sovereign."}