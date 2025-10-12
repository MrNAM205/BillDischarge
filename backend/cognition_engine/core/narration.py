import pyttsx3

def narrate(text):
    """Narrates the given text using text-to-speech."""
    try:
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"Error in narration: {e}")
