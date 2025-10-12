from flask import Flask, render_template, send_from_directory, request, jsonify
import os
import sys
import uuid
import requests

# --- Setup ---
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# --- VeroBrix Imports ---
from modules.bill_parser import BillParser

# --- Blueprints ---
from routes.document_routes import document_bp
from routes.generator_routes import generator_bp

from routes.endorsement_routes import endorsement_bp

# --- Flask App Initialization ---
app = Flask(__name__, static_folder='dist', static_url_path='/')

# Register Blueprints
app.register_blueprint(document_bp)
app.register_blueprint(generator_bp)
app.register_blueprint(endorsement_bp)

# --- API Routes ---
@app.route('/api/execute-command', methods=['POST'])
def execute_command():
    """
    Receives a command and sends it to SuperAGI to be executed by an agent.
    """
    data = request.get_json()
    command = data.get('command')

    if not command:
        return jsonify({"status": "error", "message": "No command provided"}), 400

    # --- SuperAGI Integration Logic ---
    superagi_url = "http://superagi_backend:8000/api/v1/agent"

    payload = {
      "name": f"VeroBrix Task: {command[:30]}",
      "goal": [command],
      "description": "An agent spawned from the VeroBrix Sovereign Cockpit.",
      "agent_workflow": "Goal Based Workflow",
      "constraints": ["Execute the goal and provide a clear result."],
      "model": "gpt-4",
      "max_iterations": 25
    }

    try:
        # Create the agent
        response = requests.post(superagi_url, json=payload)
        response.raise_for_status()  # Raise an exception for bad status codes
        agent_data = response.json()
        agent_id = agent_data.get("id")

        if not agent_id:
            return jsonify({"status": "error", "message": "SuperAGI did not return an agent ID.", "details": agent_data}), 500

        # Start a run for the newly created agent
        run_url = f"http://superagi_backend:8000/api/v1/agent/{agent_id}/run"
        run_response = requests.post(run_url, json={})
        run_response.raise_for_status()
        run_data = run_response.json()

        return jsonify({
            "status": "success",
            "message": f"Command sent to SuperAGI. New agent created with ID: {agent_id}. Run started.",
            "superagi_agent": agent_data,
            "superagi_run": run_data
        }), 200

    except requests.exceptions.RequestException as e:
        return jsonify({"status": "error", "message": f"Failed to connect to SuperAGI: {e}"}), 500
    except Exception as e:
        return jsonify({"status": "error", "message": f"An unexpected error occurred: {str(e)}"}), 500

@app.route('/api/parse-bill', methods=['POST'])
def parse_bill_endpoint():
    """
    Receives bill text and returns structured data.
    """
    data = request.get_json()
    bill_text = data.get('bill_text')

    if not bill_text:
        return jsonify({"status": "error", "message": "No bill_text provided"}), 400

    try:
        parser = BillParser()
        parsed_data = parser.parse_bill(bill_text)
        return jsonify({"status": "success", "parsed_data": parsed_data}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": f"An unexpected error occurred during parsing: {str(e)}"}), 500


# --- Static File Serving ---
@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def static_proxy(path):
    """Serve static files from the dist directory."""
    return send_from_directory(app.static_folder, path)


if __name__ == '__main__':
    os.makedirs('uploads', exist_ok=True)
    os.makedirs('workspace', exist_ok=True)
    
    # The old cognition engine is no longer needed.
    
    app.run(host='0.0.0.0', port=8000, debug=True)
