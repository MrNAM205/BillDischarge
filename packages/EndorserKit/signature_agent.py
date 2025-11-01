from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization
from .utils import load_config
import json

def sign_endorsement(endorsement_data):
    config = load_config('config/user_config.yaml')
    private_key_path = config.get('signature', {}).get('private_key_path')

    if not private_key_path:
        raise ValueError("Private key path not found in user_config.yaml")

    with open(private_key_path, "rb") as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None,
        )

    # Serialize the endorsement data to a consistent format
    serialized_data = json.dumps(endorsement_data, sort_keys=True).encode('utf-8')

    signature = private_key.sign(
        serialized_data,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )

    return signature