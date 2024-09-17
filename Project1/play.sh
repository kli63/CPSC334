#!/bin/bash
sudo fuser -k 8000/tcp

python3 -m http.server 8000 &

sleep 2

chromium-browser --kiosk --incognito --enable-logging=stderr --v=1 http://localhost:8000