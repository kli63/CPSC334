#!/bin/bash

python3 -m venv env
sudo pigpiod
source env/bin/activate

cd ../src/BrachioGraphCaricature
pip install -r requirements.txt

cd ../test_gui

python3 test_gui.py