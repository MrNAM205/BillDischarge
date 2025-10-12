#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

# Change to the script's directory
cd "$(dirname "$0")"

# Create a virtual environment
if [ ! -d ".venv" ]; then
    echo "--- Creating Python virtual environment ---"
    python3 -m venv .venv
fi

# Activate the virtual environment for this script
source .venv/bin/activate

echo "--- Installing Python dependencies ---"
pip install -r requirements.txt

echo "--- Downloading SpaCy language model ---"
python -m spacy download en_core_web_sm

echo "--- Creating workspace and model directories ---"
mkdir -p workspace
mkdir -p cognition_engine/models
mkdir -p cognition_engine/data

echo "--- Training initial cognition model ---"
python cognition_engine/main.py --train

echo "--- Setup complete ---"
