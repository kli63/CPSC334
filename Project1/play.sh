#!/bin/bash

python3 -m http.server &

sleep 2

chromium-browser --kiosk --incognito --enable-logging=stderr --v=1 http://localhost:8000