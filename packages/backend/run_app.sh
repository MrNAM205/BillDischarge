# packages/backend/run_app.sh

export PYTHONPATH=$PYTHONPATH:../../
export FLASK_APP=packages/backend/app.py
packages/backend/venv/bin/flask run
