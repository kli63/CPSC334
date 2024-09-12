# Previous Action Items Completed:
- [x]  create a github account (if you haven't already)
- [x]  Create a repo for 334 if you haven't already
- [x]  Create a folder in your 334 repo called raspi-ip and in that folder, a doc named ip.md
- [x]  Enable SSH [raspi-config]
- [x]  Change password for user pi [raspi-config]
- [x]  SSH into your RPi from your laptop (you will have to be on the Yale network)[CLI]
- [x]  **Generate an SSH key (or redo if yours doesn’t work)** for use with GitHub so you don't need to enter your creds to pull/push [see GitHub docs below] and add to your GitHub keys. [from Lab 1]
- [x]  **Write a bash script** that writes the current IP address to the ip.md file in your repo and (**if SSH Key is working**) uploads to github.

# New Actions: Systemd and Config File Backup
- [x]  Automate uploading so that every time the system boots, the script is run and the IP uploaded to GitHub [Systemd/.bashrc]
- [x]  Create a repo for your config files on GitHub or use same as the ip.md file
- [x]  Discover what config files are important to your system (environment) and add code to your startup script/process to copy those config files to your local config repo [CLI].
- [x]  **Push your configs** to GitHub so you can easily recreate your system functionality when your SD card fails.