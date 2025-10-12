# 🧠 Sovereign Cognition Engine: README

## Overview

This project transforms LocalAI into a sovereign, file-aware, dialogic cognition engine. It autonomously scans your workspace, classifies documents (legal, technical, financial), routes them to appropriate remedy agents, and evolves its intelligence based on your phrasing, feedback, and operational instincts.

Built entirely with free and open-source tools, this system is designed for authorship, remedy, and cockpit-grade orchestration.

---

## 🔧 Architecture

### Core Components

| Component              | Role                                                  | Tooling Used                     |
|------------------------|-------------------------------------------------------|----------------------------------|
| `LocalAI`              | NLP engine for intent classification and learning     | Python, scikit-learn, spaCy      |
| `OVB` (Omni VeroBrix)  | Sovereign agent registry and CLI trigger system       | Bash, Python, n8n (optional)     |
| `File Watcher`         | Monitors workspace for new/modified files             | `watchdog`, `inotify`, cron      |
| `PDF Classifier`       | Extracts and classifies document content              | `PyMuPDF`, `pdfminer.six`        |
| `Self-Learning Engine` | Updates cognition from feedback and phrasing logs     | `joblib`, custom Python scripts  |
| `Voice Narration`      | Speaks agent actions and insights                     | `pyttsx3`, `espeak`, `OVB speak` |
| `system_agent`         | Executes system-level shell commands                  | Python, `subprocess`             |
| `OmniDeck GUI`         | Visual cockpit for agent orchestration                | HTML/CSS/JS, Flask, Mermaid.js   |

---

## 🚀 Installation

### 1. Clone the Repositories

```bash
git clone https://github.com/your-org/localai-cognition
git clone https://github.com/your-org/ovb-core
```

### 2. Install Dependencies

```bash
pip install spacy scikit-learn pdfminer.six PyMuPDF joblib flask pyttsx3 watchdog python-magic
python -m spacy download en_core_web_sm
```

---

## 🧬 Root-Level Cognition: System Command Execution

The engine now possesses root-level cognition, allowing it to execute system commands. This is handled by the `system_agent`.

You can trigger the `system_agent` by creating a file with a `.system` extension or a file containing the `execute:` directive in the `workspace` directory.

**Example:**

1.  Create a file named `list_files.system` in the `workspace` directory.
2.  Add the following content to the file:

    ```
    execute: ls -l
    ```

3.  When the file is saved, the engine will detect it, classify it as a system command, and execute `ls -l`.

> **Security Warning:** This feature grants the engine significant control over the system. Every command is narrated, but exercise caution. The `ethics_guard` provides a layer of safety, but the ultimate responsibility for commands rests with the author.

---

## 🧬 File Awareness & Classification

### `file_watcher.py`

Monitors your workspace and triggers classification:

```python
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from classifier import classify_pdf

class Handler(FileSystemEventHandler):
    def on_created(self, event):
        if event.src_path.endswith((".pdf", ".system")):
            domain = classify_pdf(event.src_path)
            route_to_agent(domain, event.src_path)

observer = Observer()
observer.schedule(Handler(), path="/your/workspace", recursive=True)
observer.start()
```

---

## 🧠 Intent Classification

### `intent_classifier.py`

Trains and routes user inputs:

```python
from joblib import load
model = load("intent_classifier_model.joblib")

def classify(text):
    return model.predict([text])[0]
```

---

## 🗣️ Voice Narration

### `narrate.py`

```python
import pyttsx3
engine = pyttsx3.init()
engine.say("Legal document detected. Remedy agent triggered.")
engine.runAndWait()
```

---

## 🔁 Self-Learning Feedback

### `self_learning.py`

```python
def update_model(correction, original_intent):
    # Append to training set, retrain model
    pass
```

---

## 🧠 OmniDeck GUI (Optional)

Use Flask + Mermaid.js to visualize agent flows:

```html
<div class="mermaid">
graph TD
    A[File Uploaded] --> B{Classify Domain}
    B --> C[Legal → remedy_agent]
    B --> D[Tech → doc_intake_agent]
    B --> E[Finance → finance_parser_agent]
    B --> F[System → system_agent]
</div>
```

---

## 🛠️ Free Tools Used

- **Python**: Core scripting and orchestration
- **spaCy**: NLP parsing and intent detection
- **scikit-learn**: Model training and classification
- **pdfminer.six / PyMuPDF**: PDF parsing
- **watchdog / inotify**: File monitoring
- **pyttsx3 / espeak**: Voice output
- **Flask**: Web interface
- **Mermaid.js**: Flowchart visualization
- **n8n** *(optional)*: Low-code orchestration

---

## 🧠 Future Enhancements

- Semantic overlays for deeper document understanding
- Feedback ingestion from CLI logs and markdown phrasing
- GUI triggers with real-time narration
- Agent chaining for multi-step remedy protocols
- Integration with sovereign filing systems (e.g. legal complaint generators)

---

## 🧑‍💻 Authorship

This system is authored by **Daddy**, a sovereign architect of modular cognition. Every agent, every overlay, and every narration is a reflection of dialogic intelligence and ethical remedy.
