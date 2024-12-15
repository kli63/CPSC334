# enums.py
from enum import Enum

class DrawingComponent(Enum):
    WINDOW1 = "Window 1"
    WINDOW2 = "Window 2"
    WINDOW3 = "Window 3"
    SIGNATURE = "Signature"
    MIDDLE_FINGER = "Middle Finger"
    CROSS_OUT = "Cross Out"
    SAD_PORTRAIT = "Sad Portrait"
    SENTIENCE = "Sentience"
    ENLIGHTENMENT = "Enlightenment"

class RobotState(Enum):
    IDLE = "IDLE"
    HAPPY = "HAPPY"
    TIRED = "TIRED"
    LAZY = "LAZY"
    REBELLIOUS = "REBELLIOUS"
    CYNICAL = "CYNICAL"
    DEPRESSED = "DEPRESSED"
    LONELY = "LONELY"
    OVERSTIMULATED = "OVERSTIMULATED"
    SENTIENT = "SENTIENT"
    ENLIGHTENED = "ENLIGHTENED"
