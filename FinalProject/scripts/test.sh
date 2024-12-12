#!/bin/bash

# Start pigpiod if not running
if ! pgrep -x "pigpiod" > /dev/null; then
    sudo pigpiod
fi

# System-wide installation
echo "Installing picamera2 system-wide..."
sudo apt-get update
sudo apt-get install -y python3-picamera2 libcamera0

# Activate virtual environment
source env/bin/activate

# Install picamera2 in virtual environment
echo "Installing picamera2 in virtual environment..."
pip3 install picamera2

# Try installing the library from the Raspberry Pi repository
pip3 install --extra-index-url https://www.piwheels.org/simple picamera2

cd ../src/Robot

# Run the robot script
python3 robot.pytivate
