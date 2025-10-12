# VeroBrix: The Sovereign Finance Cockpit

## Vision: Sovereign Modular Intelligence

**VeroBrix** is a living, dialogic system designed to orchestrate modular agents, lawful remedy, and sovereign authorship. It is a web-based application and cognition engine that empowers individuals to take control of their financial sovereignty by analyzing financial documents, generating legal remedies, and managing interactions with creditors.

The project's core philosophy is to provide tools for autonomy, transparency, and lawful remedy, inspired by legal experts and AI archetypes.

## Project Structure

The project is organized into two main parts:

-   `frontend/`: A React-based web interface for interacting with the system.
-   `backend/`: A Python-based backend powered by Flask, which includes the core business logic, agents, and cognition engine.

## Core Features

-   **Document Analysis:** Scan and classify financial documents like bills, contracts, and statements for compliance with consumer protection laws (TILA, FCRA).
-   **Remedy Generation:** Generate legal remedy letters, dispute letters, and Cease and Desist notices for violations or inaccuracies.
-   **Bill Endorsement:** Digitally endorse bills and other financial instruments, validate their negotiability, and generate tender letters.
-   **Cognition Engine:** An autonomous engine that can scan the workspace, classify documents, and route them to appropriate agents for processing.
-   **Agent-Based Architecture:** A modular system of agents (e.g., `remedy_synthesizer`, `contradiction_engine`) that perform specific tasks.
-   **Sovereign Loop:** Track your progress through the key stages of financial remedy: Intake, Validate, Remedy, Log, and Reflect.

## High-Level Architecture

| Layer                 | Role                                                              |
| --------------------- | ----------------------------------------------------------------- |
| **LocalAI + spaCy**   | Intent parsing, semantic classification, phrasing evolution       |
| **OVB Agent Registry**| Modular CLI triggers for remedy, audit, ingestion, and system control|
| **VeroBrix Modules**  | Legal intelligence: contradiction detection, remedy synthesis     |
| **Corpus System**     | Ingests statutes, filings, manuals for semantic tagging and overlays |
| **Web Interface**     | A Flask and React-based cockpit to manage the entire process.     |

## Setup and Usage

1.  **Install Dependencies:**

    *   **Backend (Python):**
        ```bash
        pip install -r backend/requirements.txt
        ```

    *   **Frontend (Node.js):**
        ```bash
        cd frontend
        npm install
        npm run build
        cd ..
        ```

2.  **Run the Application:**

    *   **Backend:**
        ```bash
        python backend/app/app.py
        ```
        The backend will be available at `http://127.0.0.1:8000`.

    *   The frontend is served by the backend. Once the backend is running, you can access the application at `http://127.0.0.1:8000`.

---
*This README was consolidated from multiple documentation files during a project restructuring.*
