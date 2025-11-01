
import os, yaml
from datetime import datetime

EXPORT_DIR = "exports"

def load_manifest(filename):
    path = os.path.join(EXPORT_DIR, filename)
    with open(path, "r") as f:
        return yaml.safe_load(f)

def sign_manifest(filename, private_key):
    manifest = load_manifest(filename)
    manifest["signature"] = f"Signed with key {private_key[:6]}…"
    manifest["signed_at"] = datetime.utcnow().isoformat()
    manifest["lineage"]["event"] = "manifest_signed"

    signed_filename = filename.replace(".yaml", ".signed.yaml")
    path = os.path.join(EXPORT_DIR, signed_filename)
    with open(path, "w") as f:
        yaml.dump(manifest, f)
    return manifest
