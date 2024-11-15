#!/bin/bash
if ! pgrep -x "pigpiod" > /dev/null; then
    sudo pigpiod
fi

python3 -m venv env
source env/bin/activate
cd ../src/BrachioGraphCaricature
pip install -r requirements.txt

python3 run.py