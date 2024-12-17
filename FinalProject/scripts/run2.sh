#!/bin/bash

# Define base paths
BASE_DIR="/home/student334/CPSC334/FinalProject"
VENV_DIR="$BASE_DIR/env"
BRACHIO_DIR="$BASE_DIR/src/BrachioGraphCaricature"
ROBOT_DIR="$BASE_DIR/src/test_gui"

# Create virtual environment if it doesn't exist
if [ ! -d "$VENV_DIR" ]; then
    python3 -m venv "$VENV_DIR"
fi

# Start pigpiod if not running
if ! pgrep -x "pigpiod" > /dev/null; then
    sudo pigpiod
fi

# Activate virtual environment
source "$VENV_DIR/bin/activate"

# Add system Python packages to PYTHONPATH
export PYTHONPATH="/usr/lib/python3/dist-packages:$PYTHONPATH"

# Install TFLite Runtime if not already installed
if ! python3 -c "import tflite_runtime" 2>/dev/null; then
    echo "Installing TFLite Runtime..."
    pip3 install --extra-index-url https://www.piwheels.org/simple tflite-runtime
fi

# Install BrachioGraph requirements
cd "$BRACHIO_DIR"
pip install -r requirements.txt --break-system-packages

# Go to Robot directory and run
cd "$ROBOT_DIR"
python3 test.py --hardware