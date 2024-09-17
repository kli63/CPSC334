#!/bin/bash

IP=$(hostname -I | awk '{print $1}')

REPO_PATH="$HOME/CPSC334/raspberrypi"

IP_FILE="$REPO_PATH/ip.md"

echo "$IP" > "$IP_FILE"

cp /boot/config.txt "$REPO_PATH/configs"
cp ~/.bashrc "$REPO_PATH/configs"
cp /etc/fstab "$REPO_PATH/configs"
cp /etc/hostname "$REPO_PATH/configs"
cp /etc/hosts "$REPO_PATH/configs"

cd "$REPO_PATH" || exit

git config --global user.email "kli131163@gmail.com"
git config --global user.name "kli63"

git add ip.md config.txt .bashrc fstab hostname hosts

git commit -m "Update IP and config files on $(date)"

git push origin main
