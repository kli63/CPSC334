# Generative and Decaying Portraits
This is generative art display is a play on [Conway's Game of Life](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life), using images of [human portraits](https://www.kaggle.com/datasets/arnaud58/flickrfaceshq-dataset-ffhq/data?select=00031.png) as the initial state. The generative aspect of this art piece is derived from a few aspects of the project's implementation. First, is a slight subversion of Conway's Game of Life, which is famously deterministic and not generative. Although my project maintains the basic rules of life and death within the game, it also introduces randomness into the survival and death of the cells through the addition of uniquely generated health, aging, and fitness functions for each cell. These factors, as well as some degree of luck, ultimately help play into whether or not a certain cell will become alive or dead. Newly alive cells start with increased health and fitness, making them more resilient, while aging cells gradually lose fitness and become more prone to death, adding a layer of stochasticity to the traditionally predictable ruleset. Furthermore, the order of the portraits themselves are randomly selected. Lastly, the transition between the faces is generative and unpredictable, as the portraits gradually morph from one face to the next in a dynamic transition stage where cells in the grid randomly move toward the new initial state. As a result, no two iterations of this piece will ever be the same, and the portraits will fade, deform, and transform continuously as an allusion to nature and life's memory, decay, and cyclic ephemerality. 

# Links
Starting on Boot: https://youtu.be/q375IicIMTA \
256x256: https://youtu.be/GD1Niac8U8c \
512x512: https://youtu.be/EDJGp88Q70I

# Usage:
This project was designed to be compatible with a Raspberry Pi, so some of these instructions are directly related to running it on boot for your Pi. This project is of course usable without a Pi, given that you run it on some Linux system (I was developing this on WSL), and you may disregard any instructions as you see fit.

1. Clone this repo into your Raspberry Pi (or whatever local machine).
2. cd into the `/CPSC334/Project1/scripts` folder and run `sudo chmod +x play.sh`
3. To run the art piece manually, you can simply run `./play.sh`, and a chromium browser will open and play.
4. To run this art piece on boot of the Raspberry pi:
    - cd into the `/etc/systemd/system` folder and run `sudo nano play.service`. You can simply copy the contents of `/CPSC334/Project1/scripts/play.service` here.
    - Do the following commands:
        - `sudo systemctl daemon-reload`
        - `sudo systemctl enable play.service`
    - Do the following commands:
        - `sudo systemctl start play.service`
        - `sudo systemctl status play.service`
5. You should now be able to reboot your Pi, and this program will start on boot (see video to see that process working in live video)
