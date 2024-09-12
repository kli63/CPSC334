#!/bin/bash

IP=$(hostname -I | awk '{print $1}')

FILE_PATH="$HOME/CPSC334/raspberrypi/ip.md"

echo $IP > $FILE_PATH

cd "$HOME/CPSC334/raspberrypi" || exit

git config --global user.email "kli131163@gmail.com"
git config --global user.name "kli63"

git add ip.md

git commit -m "Update IP Address on $(date)"

git push origin main