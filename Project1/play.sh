#!/bin/bash

python3 -m http.server &

sleep 2

chromium-browser --kiosk --incognito http://localhost:8000