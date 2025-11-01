
import os, yaml
from datetime import datetime

CORPUS_DIR = "data/trust_corpus"
EXPORT_DIR = "exports"

def load_entry(filename):
    path = os.path.join(CORPUS_DIR, filename)
    # Ensure the directory exists before trying to read from it
    if not os.path.exists(path):
        return None
    with open(path, "r") as f:
        # Safely load YAML content
        try:
            return yaml.safe_load(f)
        except yaml.YAMLError as e:
            print(f"Error loading YAML from {filename}: {e}")
            return None

def export_manifest(files):
    # Create EXPORT_DIR if it doesn't exist
    if not os.path.exists(EXPORT_DIR):
        os.makedirs(EXPORT_DIR)

    entries = [load_entry(f) for f in files if f is not None]
    # Filter out None entries that may result from file read errors
    entries = [entry for entry in entries if entry is not None]

    manifest = {
        "type": "Trust Manifest",
        "timestamp": datetime.utcnow().isoformat(),
        "entries": entries,
        "lineage": {
            "event": "manifest_exported",
            "count": len(entries)
        }
    }
    timestamp_str = manifest['timestamp'].replace(':', '-').split('.')[0]
    filename = f"{timestamp_str}-trust_manifest.yaml"
    path = os.path.join(EXPORT_DIR, filename)
    with open(path, "w") as f:
        yaml.dump(manifest, f, default_flow_style=False, sort_keys=False)
    return manifest
