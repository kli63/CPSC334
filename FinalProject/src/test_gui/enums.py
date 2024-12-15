# enums.py
from enum import Enum

class DrawingComponent(Enum):
    WINDOW1 = "Window 1"
    WINDOW2 = "Window 2"
    WINDOW3 = "Window 3"
    SIGNATURE = "Signature"

class DrawingBehavior(Enum):
    REBELLIOUS = "Rebellious"
    CYNICAL = "Cynical"
    DEPRESSED = "Depressed"
    SENTIENT = "Sentient"
    ENLIGHTENED = "Enlightened"
    LONELY = "Lonely"

class RobotState(Enum):
    IDLE = "IDLE"
    HAPPY = "HAPPY"
    TIRED = "TIRED"
    LAZY = "LAZY"
    REBELLIOUS = "REBELLIOUS"
    CYNICAL = "CYNICAL"
    DEPRESSED = "DEPRESSED"
    LONELY = "LONELY"
    SENTIENT = "SENTIENT"
    ENLIGHTENED = "ENLIGHTENED"
    OVERSTIMULATED = "OVERSTIMULATED"
