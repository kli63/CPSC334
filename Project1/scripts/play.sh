#!/bin/bash

# install_if_missing() {
#   if ! dpkg -s "$1" >/dev/null 2>&1; then
#     echo "Installing $1..."
#     sudo apt-get update
#     sudo apt-get install -y "$1"
#   else
#     echo "$1 is already installed."
#   fi
# }

# install_if_missing python3
# install_if_missing python3-pip
# install_if_missing xdotool
# install_if_missing wmctrl
# install_if_missing chromium-browser

sudo fuser -k 8000/tcp

cd /home/student334/CPSC334/Project1

python3 -m http.server 8000 &

if [ -z "$DISPLAY" ]; then
  export DISPLAY=:0
fi

exec chromium-browser --kiosk --incognito --disable-restore-session-state --enable-logging=stderr --v=1 http://localhost:8000

# sleep 5

# xdotool search --onlyvisible --class "chromium" windowactivate --sync key F11

# wmctrl -r Chromium -b add,fullscreen
