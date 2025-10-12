from core.narration import narrate
import os

def check_corpus_alignment(text, domain):
    """
    Checks the text for alignment with the legal and philosophical corpus.
    This is a placeholder for a more sophisticated implementation.
    """
    narrate(f"Checking corpus alignment for domain: {domain}")
    
    corpus_path = f"corpus/{domain}"
    if not os.path.exists(corpus_path):
        print(f"[Ethics Guard] Corpus for domain '{domain}' not found.")
        return True # Default to aligned if corpus is not present

    # In a real implementation, this would involve searching the corpus
    # for relevant documents and comparing the text for alignment.
    # For now, we'll just do a simple keyword check.
    
    if domain == "legal":
        # Example check for legal domain
        if "unlawful" in text.lower():
            narrate("Warning: Text may contain unlawful content.")
            return False
            
    if domain == "philosophical":
        # Example check for philosophical domain
        if "unethical" in text.lower():
            narrate("Warning: Text may contain unethical content.")
            return False

    return True


def handle_ethics_guard(file_path, reason):
    """Handles ethical concerns and flags potential issues."""
    narrate(f"Ethics guard flagged file: {file_path} for reason: {reason}")
    # Placeholder for ethics guard logic
    # e.g., log concern, notify user
    print(f"[Ethics Guard] Flagged {file_path}. Reason: {reason}")

    try:
        with open(file_path, 'r') as f:
            content = f.read()
        
        # Example of using the corpus alignment check
        if not check_corpus_alignment(content, "legal"):
            print(f"[Ethics Guard] File {file_path} may not be legally aligned.")
        
        if not check_corpus_alignment(content, "philosophical"):
            print(f"[Ethics Guard] File {file_path} may not be philosophically aligned.")

    except Exception as e:
        print(f"[Ethics Guard] Error reading file {file_path}: {e}")
