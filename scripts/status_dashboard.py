import subprocess
import requests
import json

def get_active_env():
    try:
        result = subprocess.run(["poetry", "env", "info", "-p"], capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return "Not in a poetry environment."

def get_backend_health():
    try:
        response = requests.get("http://localhost:8000/api/status")
        if response.status_code == 200:
            return response.json()
        else:
            return {"status": f"Error: Received status code {response.status_code}"}
    except requests.exceptions.ConnectionError:
        return {"status": "Backend not running."}

def main():
    print("--- Sovereign Cockpit Status ---")
    
    # Active Environment
    active_env = get_active_env()
    print(f"[*] Active Environment: {active_env}")

    # Port
    print("[*] Port: 8000 (default)")

    # Backend Health
    health_status = get_backend_health()
    print("[*] Backend Health:")
    print(f"  - Status: {health_status.get('status', 'N/A')}")
    print(f"  - Last Model: {health_status.get('last_model', 'N/A')}")
    print(f"  - Last Cognition: {health_status.get('last_thoughts', 'N/A')}")
    print(f"  - Fallback: {health_status.get('fallback', 'N/A')}")
    
    print("------------------------------")

if __name__ == "__main__":
    main()
