#!/bin/bash

sudo fuser -k 8000/tcp

cd "/home/student334/installation/CPSC334/P3_Installation_Art/Creative Task/scripts"

python3 server.py &

cd "/home/student334/installation/CPSC334/P3_Installation_Art/Creative Task/src"

python3 -m http.server 8000 &

if [ -z "$DISPLAY" ]; then
  export DISPLAY=:0
fi

unclutter -idle 0 &

exec chromium-browser --kiosk --incognito --disable-restore-session-state --enable-logging=stderr --v=1 http://localhost:8000
