#!/bin/bash

IP=$(hostname -I | awk '{print $1}')

FILE_PATH="$HOME/334/raspberrypi/ip.md"

echo $IP > $FILE_PATH

cd "$HOME/334/raspberrypi" || exit

git add ip.md

git commit -m "Update IP Address on $(date)"

git push origin main
