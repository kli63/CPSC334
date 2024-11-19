# Robot Caricaturist
This project combines a BrachioGraph (inspired from here) with a camera and GUI that allows users to take their own photos, which are then vectorized into the proper format, before sent to the little destitute robot to be drawn. The enclosure of the project is built to look like a cute little robot, a face and a cup for tips all included! The BrachioGraph itself is constructed using very simple materials, using a popsicle stick, three servo motors, a clothespin, and a very fancy shmancy pen. All the code and motors are connected to a Raspberry Pi, which is the only other hardware component required for the project aside from the motors and the camera.

The BrachioGraph portion of the code is adapted from this repo, although had to be largely adjusted in order to align with the goals of my particular project (also some of the stuff was pretty outdated, so it had to be updated to the specific hardware requirements of my machine). Integrating the camera was the other big portion of the project, including both the logic of getting the camera running, as well as the GUI that acts as the user-facing platform through which users / art enjoyers can interact with this sculpture.

The overall motivation for this project is that I really really really liked BrachioGraphs and robotics! One of the most interesting art pieces that I’ve seen is “Can’t Help Myself” which shows an industrial robot continuously sweeping a blood-like substance on the floor, but continuously degrading in its efficiency and capabilities over time. Given how long the BrachioGraph takes to draw a particular image, I think there are some innate mirroring's between my project and that piece, which I ultimately didn’t connect with until sitting back down to write this portfolio post. My particular sculpture is much more light-hearted and comical take on that particular piece, and I hope acts as a commentary on the relationship between humans and machinery, especially as we head into a future that is increasingly mechanized and digitalized. Our relationship with labor is something that is always in flux and continuously in stress, and I want this project to be an extension of that conversation. 

# Links
- Starting on Boot: https://youtu.be/pbEAQ4QZwMI
- Demo: [https://www.youtube.com/watch?v=VVvQ_j8IW10](https://youtu.be/ZoBj25JuZJ0)


# Usage
This project is designed to be implemented and ran solely on a Raspberry Pi. Exact instructions may vary depending on your device and its system settings / OS.


1. Clone this repo into your Raspberry Pi. You may have to download Git LFS
  - `git lfs install`
2. Install dependencies. The main ones for this game are:
  - `sudo apt install -y python3-venv python3-tk pigpiod libjbig0 libjpeg-dev liblcms2-2 libopenjp2-7 libtiff5-dev libwebp-dev libwebpdemux2 libwebpmux3 libzstd1 libatlas3-base libgfortran5`
  - `sudo apt install python3-picamera2`
  - `sudo apt install libcamera-apps`
  - `sudo apt install python3-opencv`
  - `sudo apt install python3-pil python3-opencv python3-picamera2`
  - `sudo apt install python3-pil python3-pil.imagetk`
  - `sudo apt install git-lfs`
  - `sudo apt install python3-cairosvg`
3. Follow the instructions for installing the camera based on your device: https://docs.arducam.com/Raspberry-Pi-Camera/Native-camera/5MP-OV5647/
4. cd into the `/CPSC334/Module4/CreativeTask/Scripts` folder and run `sudo chmod +x *`
5. To run the program manually, you can simply run `./run.sh`
6. To run this program on boot of the Raspberry pi:
    - run `sudo nano /etc/systemd/system/robot-drawer.service`. You can simply copy the contents of `/CPSC334/Module2/CreativeTask/scripts/robot-drawer.service` here.
    - Do the following commands:
        - `sudo systemctl daemon-reload`
        - `sudo systemctl enable robot-drawer.service`
    - Do the following commands:
        - `sudo systemctl start robot-drawer.service`
        - `sudo systemctl status robot-drawer.service`
7. You should now be able to reboot your Pi, and this program will start on boot (see video to see that process working in live video)


# Citations
- https://www.brachiograph.art/
- https://github.com/evildmp/BrachioGraph
