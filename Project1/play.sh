#!/bin/bash
sudo apt-get install wmctrl

xset s off
xset -dpms

sudo fuser -k 8000/tcp

python3 -m http.server 8000 &

sleep 2

if [ -z "$DISPLAY" ]; then
    startx
fi

chromium-browser --kiosk --start-fullscreen --disable-gpu --incognito http://localhost:8000 &

sleep 5

wmctrl -r Chromium -b add,fullscreen
