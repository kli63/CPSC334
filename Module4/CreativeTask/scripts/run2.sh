#!/bin/bash

Environment=DISPLAY=:0

# Start pigpiod if not running
if ! pgrep -x "pigpiod" > /dev/null; then
    sudo pigpiod
fi

# Activate virtual environment
source env/bin/activate

# Add system Python packages to PYTHONPATH
export PYTHONPATH="/usr/lib/python3/dist-packages:$PYTHONPATH"

# Install TFLite Runtime if not already installed
if ! python3 -c "import tflite_runtime" 2>/dev/null; then
    echo "Installing TFLite Runtime..."
    # Get Python version
    python_version=$(python3 -c 'import sys; print(f"{sys.version_info[0]}.{sys.version_info[1]}")')
    
    # Install TFLite Runtime from piwheels
    pip3 install --extra-index-url https://www.piwheels.org/simple tflite-runtime
fi

cd ../src/BrachioGraphCaricature
pip install -r requirements.txt

cd ../Robot

# Run the robot script
python3 run.py