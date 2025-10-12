import pyttsx3
from modules.config_manager import config_manager
from modules.logger import system_logger

class VoiceNarrator:
    def __init__(self):
        self.enabled = config_manager.get('narrator.enabled', True)
        self.engine = None
        if self.enabled:
            try:
                self.engine = pyttsx3.init()
            except Exception as e:
                system_logger.error(f"Failed to initialize text-to-speech engine: {e}")
                self.engine = None

    def say(self, text):
        system_logger.info(f"Narrator: {text}")
        if self.enabled and self.engine:
            self.engine.say(text)
            self.engine.runAndWait()

# Singleton instance
narrator = VoiceNarrator()