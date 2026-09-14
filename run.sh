#!/bin/bash
set -e

# Create venv if missing
if [ ! -d "venv" ]; then
    echo "First-time setup: Creating virtual environment..."
    python3 -m venv venv
fi

# Activate venv
source venv/bin/activate

# Install dependencies if needed
if [ -f "requirements.txt" ]; then
    python3 -m pip install -q -r requirements.txt
fi

# Launch app
echo "Launching MidleCode Studio..."
python main/main.py
