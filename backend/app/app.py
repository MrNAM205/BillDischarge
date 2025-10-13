from flask import Flask, render_template, send_from_directory, request, jsonify
import os
import sys
import uuid
import requests

# --- Setup ---
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# --- Blueprints ---
from routes.endorsement_routes import endorsement_bp
# from routes.document_routes import document_bp
# from routes.generator_routes import generator_bp

# --- Flask App Initialization ---
app = Flask(__name__, static_folder='dist', static_url_path='/')

# Register Blueprints
app.register_blueprint(endorsement_bp)
# app.register_blueprint(document_bp)
# app.register_blueprint(generator_bp)


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
    
    app.run(host='0.0.0.0', port=8000, debug=True)
