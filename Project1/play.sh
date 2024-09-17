#!/bin/bash
sudo fuser -k 8000/tcp

python3 -m http.server 8000 &

if [ -z "$DISPLAY" ]; then
  export DISPLAY=:0
fi

chromium-browser --kiosk --incognito --disable-restore-session-state --enable-logging=stderr --v=1 http://localhost:8000 &

# sleep 5

xdotool search --onlyvisible --class "chromium" windowactivate --sync key F11

wmctrl -r Chromium -b add,fullscreen
