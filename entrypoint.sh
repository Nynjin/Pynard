#!/bin/bash

if [ ! -f /app/.venv/bin/activate ]; then
    echo "Creating virtual environment..."
    python -m venv .venv
fi
source .venv/bin/activate

python -m pip install -r requirements.txt

python demo.py