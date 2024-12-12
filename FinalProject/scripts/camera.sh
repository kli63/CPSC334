#!/bin/bash

fuser -k /dev/video0

cd ../src/Camera

python3 camera.py

fuser -k /dev/video0
