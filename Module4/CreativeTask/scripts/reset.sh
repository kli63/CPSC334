#!/bin/bash

sudo pigpiod
cd ../src/BrachioGraphCaricature
source env/bin/activate

python3 reset.py

