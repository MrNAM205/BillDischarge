# VeroBrix Development Documentation

This file consolidates documents related to the development, architecture, and improvement of the VeroBrix system.

---
---

# Part 1: Agent Architecture

## Agent Framework Overview

VeroBrix employs a modular agent architecture where each agent represents a distinct intelligence overlay with specialized capabilities. This design allows for both fictional AI archetypes and real-world legal expertise to be integrated seamlessly.

### Core Agent Principles
1.  **Modular Intelligence:** Each agent operates independently with defined interfaces.
2.  **Provenance Tracking:** Every agent action is logged with full provenance and signatures.
3.  **Sovereignty Alignment:** All agents evaluate outputs for sovereignty alignment, flagging "servile language."

## Active Agent Profiles

### JARVIS Agent
-   **Role**: Procedural, logical, system-integrated analysis.
-   **Capabilities**: Advanced clause extraction, multi-pattern contradiction detection, legal structure analysis.

### FRIDAY Agent
-   **Role**: Emotional, tactical, conversational intelligence.
-   **Capabilities**: Legal-context sentiment analysis, risk assessment, comprehensive legal summaries.

### Ultron Agent
-   **Role**: Autonomous, predictive, cautionary analysis.
-   **Capabilities**: Predictive analysis of legal outcomes, autonomous decision-making recommendations.

### Dialogos Agent
-   **Role**: Philosophical overlays, authorship prompts.
-   **Capabilities**: Philosophical analysis of legal concepts, authorship integrity checking.

---
---

# Part 2: Development Guide

## Getting Started

### Prerequisites
-   Python 3.7+
-   Git
-   Virtual environment (venv, conda, etc.)

### Quick Setup
```bash
# Clone the repository
git clone <repository-url>
cd VB

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Download spaCy model
python -c "import spacy; spacy.cli.download('en_core_web_sm')"

# Test the installation
python verobrix_cli.py --version
```

## Testing Framework
-   **Run tests:** `python -m pytest tests/ -v`
-   **Test Categories:** Unit, Integration, Performance, and Sovereignty tests.

## Configuration Management
-   The system uses a centralized `config/verobrix.yaml` file for managing settings related to NLP, agents, logging, and sovereignty scoring.

## Agent Development
-   New agents should be created in their own directory under `agents/` and implement a base agent interface.
-   All agents must integrate with the provenance logger and sovereignty scorer.

---
---

# Part 3: Improvement Recommendations

## High Priority Improvements
1.  **Enhanced Natural Language Processing:** Integrate advanced NLP libraries (spaCy, NLTK, Transformers) for more accurate entity extraction, semantic analysis, and contradiction detection.
2.  **Database Integration for Legal Corpus:** Move from static files to a database (SQLite/PostgreSQL) for faster, more advanced searching of the legal corpus.
3.  **Configuration Management System:** Centralize all hard-coded settings into a YAML/JSON configuration system.
4.  **Enhanced Error Handling and Logging:** Implement comprehensive, structured logging and custom exception classes.

## Medium Priority Improvements
5.  **Web-Based User Interface:** Create a modern web UI using a framework like Flask/FastAPI + React/Vue.
6.  **Advanced Legal Document Templates:** Use a templating engine like Jinja2 for more sophisticated and conditional document generation.
7.  **Machine Learning Integration:** Introduce ML models for legal outcome prediction and risk assessment.
8.  **API Development:** Create a RESTful API to allow for integration with other tools.

---
---

# Part 4: High-Level Build Steps

### Step 1: Create the Local Server (The Backend)
-   **File Reading:** The server must be able to read the contents of the user's local files and folders to provide context.
-   **Prompt Generation:** The server combines the user's request with the local file context to create a structured prompt for the AI model.
-   **API Management:** The server manages API calls to the AI model, handling errors and network issues.

### Step 2: Build the IDE Extension (The Frontend)
-   **Editor Integration:** The extension reads what the user is typing in real-time.
-   **Event Handling:** Implement debouncing to prevent sending an API request for every keystroke.
-   **Rendering Suggestions:** Display the AI's response as "ghost text" suggestions in the editor.
-   **Chat Interface:** A panel for conversational interaction with the AI.

### Step 3: Integrate a Large Language Model (The Brain)
-   **API Calls:** The local server makes calls to the LLM's API (e.g., Gemini).
-   **Token Management:** The system must manage the context size to stay within the model's input limits.
