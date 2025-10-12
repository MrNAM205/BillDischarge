import magic
from pdfminer.high_level import extract_text
from joblib import load

def classify_text(text):
    """Classifies text using a pre-trained model."""
    # Rule for system commands
    if text.strip().startswith("execute:"):
        return "system"

    try:
        model = load('models/intent_classifier_model.joblib')
        # The model expects a list of texts
        prediction = model.predict([text])
        return prediction[0]
    except FileNotFoundError:
        print("Classifier model not found. Please train the model first.")
        # Return a default or generic domain if the model is not available
        if 'dispute' in text.lower() or 'legal' in text.lower():
            return 'legal'
        elif 'technical' in text.lower() or 'config' in text.lower():
            return 'technical'
        elif 'financial' in text.lower() or 'invoice' in text.lower():
            return 'financial'
        return 'unknown'
    except Exception as e:
        print(f"An error occurred during classification: {e}")
        return 'unknown'

def classify_file(file_path):
    """Classifies a file based on its content."""
    try:
        # Rule for system command files
        if file_path.endswith(".system"):
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                text = f.read()
            return classify_text(text)

        mime = magic.from_file(file_path, mime=True)
        print(f"Classifying file: {file_path} with mime type: {mime}")
        if "pdf" in mime:
            text = extract_text(file_path)
            return classify_text(text)
        elif "text" in mime:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                text = f.read()
            return classify_text(text)
        else:
            print(f"Unsupported file type: {mime}")
            return None
    except Exception as e:
        print(f"An error occurred during file classification: {e}")
        return None
