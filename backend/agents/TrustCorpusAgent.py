
import os, yaml
from datetime import datetime

CORPUS_DIR = "data/trust_corpus"

def list_corpus_entries():
    index_path = os.path.join(CORPUS_DIR, "corpus_index.yaml")
    if not os.path.exists(index_path):
        return []
    with open(index_path, "r") as f:
        return yaml.safe_load(f) or []

def add_entry(title, content):
    timestamp = datetime.utcnow().isoformat()
    filename = f"{timestamp[:19].replace(':', '-')}-{title.replace(' ', '_')}.yaml"
    path = os.path.join(CORPUS_DIR, filename)
    with open(path, "w") as f:
        f.write(content)

    entry = { "title": title, "timestamp": timestamp, "file": filename }
    index = list_corpus_entries()
    index.append(entry)
    with open(os.path.join(CORPUS_DIR, "corpus_index.yaml"), "w") as f:
        yaml.dump(index, f)
    return entry
