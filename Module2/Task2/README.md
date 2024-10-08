# Foxy's Adventure
This project is a 2D sidescrolling game built using pygame, and designed to be played on a Raspberry Pi with RPi.GPIO and an ESP32 using serial. The motivation for this project is several-fold: 1. I really like games! I've always been interested in building games, and since I'm taking Creative Embedded Systems concurrently with Yale's new Game Engines course, I thought that this would be a great opportunity to challenge myself to create a game, and have it be playable on the Raspberry Pi. Having had experience from the previous labs, using the physical hardware resources (analog joystick, SPST switch, and a momentary button) was honestly the easiest portion of the project, and I had always had a rough general idea of what my physical controller and enclosure/device would look like. As a result, I dedicated a signficant portion of time to just creating the game, which definitely took the vast majority of this project's time. The game utilizes physical hardware components to control the playable character and the game's various mechanics, although the user can also connect a keyboard and mouse to the Pi to play as well. Game mechanics include those found in very basic sidescrolling games, such as 2D movement, platforming, different types of attacking, and AI enemies. The game is designed to be scalable (YAY OBJECT ORIENTED PROGRAMMING), meaning that further levels can be easily designed, and additional challenges and functionalities can be added on top of the existing codebase. 

# Links
- Starting on Boot: https://www.youtube.com/watch?v=ZleiavgJ4AA
- PC Gameplay: https://www.youtube.com/watch?v=VVvQ_j8IW10
- Raspberry Pi Gameplay: https://www.youtube.com/watch?v=UBYsndD7iPk
- Live Commentary - https://www.youtube.com/watch?v=Q4N2ATut_7Y

# Usage
This project was designed to be compatible with a Raspberry Pi, so some of these instructions are directly related to running it on boot for your Pi. This project is of course usable without a Pi, given that you run it on some Linux system (I was developing this on WSL), and you may disregard any instructions as you see fit. This game is also playable on any PC, given that you have the proper dependencies involved: `python3 pc-game.py`


1. Clone this repo into your Raspberry Pi (or whatever local machine).
2. Install dependencies. The main ones for this game are:
  - `sudo apt-get install python3-RPi.GPIO`
  - `sudo apt-get install python3-pygame`
  - `sudo apt-get install python3-serial`
3. cd into the `/CPSC334/Project2/scripts` folder and run `sudo chmod +x run-game.sh`
4. To play the game manually, you can simply run `./run-game.sh`, or in the `/CPSC334/Module2/Task2/src` directory, run `python3 game.py`.
5. To run this game on boot of the Raspberry pi:
    - cd into the `/etc/systemd/system` folder and run `sudo nano run-game.service`. You can simply copy the contents of `/CPSC334/Module2/Task2/scripts/run-game.service` here.
    - Do the following commands:
        - `sudo systemctl daemon-reload`
        - `sudo systemctl enable run-game.service`
    - Do the following commands:
        - `sudo systemctl start run-game.service`
        - `sudo systemctl status run-game.service`
6. You should now be able to reboot your Pi, and this game will start on boot (see video to see that process working in live video


# Citations
I utilized a few free sprites and texture packs for this project, and I've listed them here:
- https://caz-creates-games.itch.io/cute-bomb-character-sprite
- https://flippurgatory.itch.io/animated-potion-assets-pack-free
- https://ansimuz.itch.io/sunny-land-pixel-game-art
- https://xzany.itch.io/flying-demon-2d-pixel-art
