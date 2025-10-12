# VeroBrix / OmniDeck Brainiac: Technical Roadmap

This document consolidates the technical roadmaps and architecture from various README files for the VeroBrix project, also known as OmniDeck Brainiac and Sovereign Cognition Engine.

---

## Phased Development Plan

This plan outlines the evolution of the AI assistant from basic integration to a fully autonomous, on-call agent.

### Phase 1-4: Foundational Intelligence & Action
- **Goal:** Establish core agents (`Dialogos`), integrate local LLMs, enable code generation (`CodeSmith`), and add internet search (`ContextWeaver`). This phase also includes developing a "Dialogic Growth Engine" for persistent memory and provenance.

### Phase 5: Deep System Integration
- **Goal:** Enable the AI to securely access and interact with the host operating system (files, processes, system info).
- **Tools:** `psutil` for system monitoring, `os` and `shutil` for file management, `subprocess` for process management.

### Phase 6: Autonomous System Maintenance
- **Goal:** Enable the AI to perform autonomous tasks like file deduplication and software package management (`pip`, `apt`, etc.).

### Phase 7: On-Call Assistant
- **Goal:** Transform the AI into a persistent, on-call assistant activated by keyword or system events.
- **Tools:** `speech_recognition` and `pyaudio` for keyword activation.
- **Implementation:** Run as a background service or `systemd` daemon on Linux.

### Phase 8: Interactive Communication
- **Goal:** Allow the AI to understand instructions from uploaded Markdown files or direct voice commands.

---

## Architecture Overview

The system is designed as a "s-overeign, file-aware, dialogic cognition engine" that transforms a local AI into an autonomous agent.

### Core Components

| Component | Role | Tooling |
|---|---|---|
| **LocalAI** | NLP engine for intent classification and learning | Python, scikit-learn, spaCy |
| **OVB (Omni VeroBrix)** | Sovereign agent registry and CLI trigger system | Bash, Python |
| **File Watcher** | Monitors workspace for new/modified files | `watchdog`, `inotify` |
| **PDF Classifier** | Extracts and classifies document content | `PyMuPDF`, `pdfminer.six` |
| **Self-Learning Engine**| Updates cognition from feedback and logs | `joblib`, custom scripts |
| **Voice Narration** | Speaks agent actions and insights | `pyttsx3`, `espeak` |
| **System Agent** | Executes system-level shell commands | Python, `subprocess` |
| **OmniDeck GUI** | Visual cockpit for agent orchestration | Flask, Mermaid.js |

---

## Installation and Setup

### Prerequisites
- Python 3.7+
- Git

### Installation Steps
1.  **Clone the repository.**
2.  **Create a virtual environment:** `python -m venv venv`
3.  **Install dependencies:** `pip install -r requirements.txt` (Note: A consolidated `requirements.txt` would need to be created).
    *   Key dependencies mentioned: `spacy`, `scikit-learn`, `pdfminer.six`, `PyMuPDF`, `joblib`, `flask`, `pyttsx3`, `watchdog`, `psutil`, `speech_recognition`, `pyaudio`.
4.  **Download NLP models:** `python -m spacy download en_core_web_sm`

### Usage
The system can be run via a main launcher script or a command-line interface.

```bash
# Example from one of the READMEs
python verobrix_cli.py -f path/to/document.txt
```
