
import os, yaml, hashlib
from datetime import datetime
import requests

EXPORT_DIR = "exports"
PUBLISHED_DIR = "published"

def load_signed_manifest(filename):
    path = os.path.join(EXPORT_DIR, filename)
    with open(path, "r") as f:
        return yaml.safe_load(f)

def publish_manifest(filename, registry_url):
    manifest = load_signed_manifest(filename)
    manifest_hash = hashlib.sha256(yaml.dump(manifest).encode()).hexdigest()

    # Simulate publication
    try:
        response = requests.post(registry_url, json={
            "manifest": manifest,
            "hash": manifest_hash
        })
        status_code = response.status_code
    except requests.exceptions.RequestException as e:
        print(f"Error publishing manifest: {e}")
        status_code = -1

    receipt = {
        "published_at": datetime.utcnow().isoformat(),
        "hash": manifest_hash,
        "registry": registry_url,
        "status": status_code
    }

    # Save locally
    if not os.path.exists(PUBLISHED_DIR):
        os.makedirs(PUBLISHED_DIR)
        
    published_filename = filename.replace(".signed.yaml", ".published.yaml")
    path = os.path.join(PUBLISHED_DIR, published_filename)
    with open(path, "w") as f:
        yaml.dump({ "manifest": manifest, "receipt": receipt }, f)

    return receipt
