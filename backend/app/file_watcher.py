
import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from modules.voice_narrator import narrator
from modules.nlp_processor import nlp_processor
from modules.logger import system_logger, log_provenance
from modules.config_manager import config_manager

# Dynamically import agents based on config
jarvis_agent = None
if config_manager.get('agents.jarvis.enabled', False):
    from agents.jarvis_agent import jarvis_agent

friday_agent = None
if config_manager.get('agents.friday.enabled', False):
    from agents.friday_agent import friday_agent

dialogos_agent = None
if config_manager.get('agents.dialogos.enabled', False):
    from agents.dialogos_agent import dialogos_agent

class IntakeHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            system_logger.info(f"New file detected: {event.src_path}")
            narrator.say("New document detected.")
            self.process_file(event.src_path)

    def process_file(self, file_path):
        try:
            # Wait a moment for the file to be fully written
            time.sleep(1)
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            log_provenance("IntakeHandler", "ProcessFile", f"Processing {file_path}")

            # Process with NLP
            nlp_results = nlp_processor.process_text(content)
            narrator.say(f"Document classified as {nlp_results['classification']}.")

            # Route to enabled agents
            if jarvis_agent:
                jarvis_agent.analyze(file_path, nlp_results)
            
            if friday_agent:
                friday_agent.analyze(file_path, content)

            if dialogos_agent:
                dialogos_agent.analyze(content)

        except Exception as e:
            system_logger.error(f"Error processing {file_path}: {e}")
            narrator.say("Error processing document.")

def start_watching(path):
    event_handler = IntakeHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=False)
    
    system_logger.info(f"Starting to watch directory: {path}")
    narrator.say(f"Watching the {os.path.basename(path)} directory.")
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        system_logger.info("File watcher stopped by user.")
        narrator.say("File watcher stopped.")
    observer.join()
