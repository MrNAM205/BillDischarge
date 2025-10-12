import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from core.classifier import classify_file
from core.narration import narrate
from agents.remedy_agent import handle_remedy
from agents.doc_intake_agent import handle_doc_intake
from agents.ethics_guard import handle_ethics_guard
from agents.system_agent import handle_system_command
from agents.situation_interpreter import interpret_situation
from agents.remedy_synthesizer import synthesize_remedy
from agents.contradiction_engine import detect_contradiction

def route_to_agent(domain, file_path):
    narrate(f"File detected with domain: {domain}. Routing to appropriate agent.")
    
    if domain == "legal":
        # Full cognition loop for legal domain
        situation = interpret_situation(file_path)
        remedy_path = synthesize_remedy(file_path, situation)
        
        with open(file_path, 'r') as f:
            content = f.read()
        contradictions = detect_contradiction(file_path, content)
        
        narrate(f"Legal cognition loop complete. Remedy drafted at {remedy_path}. Contradictions found: {len(contradictions)}")
        # Further actions can be taken based on the remedy and contradictions
        
    elif domain == "technical":
        handle_doc_intake(file_path)
    elif domain == "financial":
        # Placeholder for financial agent
        narrate("Financial agent not yet implemented.")
    elif domain == "system":
        handle_system_command(file_path)
    else:
        handle_ethics_guard(file_path, f"Unknown domain: {domain}")

class Handler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            print(f"New file created: {event.src_path}")
            domain = classify_file(event.src_path)
            if domain:
                route_to_agent(domain, event.src_path)

def start_file_watcher(path):
    observer = Observer()
    observer.schedule(Handler(), path=path, recursive=True)
    observer.start()
    narrate("Sovereign cognition daemon activated. Monitoring workspace.")
    print(f"Watching directory: {path}")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
    narrate("Sovereign cognition daemon deactivated.")

