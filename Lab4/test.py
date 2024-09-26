from gpiozero import Button, LED
from signal import pause
import time

button = Button(2)  # Momentary button to toggle game on/off
switch = Button(3)  # SPST Switch for actions
joystick_x = Button(14)  # Joystick X direction (simulate left/right)
joystick_y = Button(15)  # Joystick Y direction (simulate vertically/down)
joystick_button = Button(18)  # Joystick button for jump (SW)

led = LED(17)

game_on = False
mode = 0
press_start_time = 0  
game_off_message_printed = False 

def button_pressed():
    global press_start_time
    press_start_time = time.time()

    while button.is_pressed:
        press_duration = time.time() - press_start_time
        if press_duration > 1.0:
            global game_on
            game_on = not game_on
            print("Game started!" if game_on else "Game stopped!")
            break

def button_released():
    global mode
    press_duration = time.time() - press_start_time

    if press_duration <= 1.0 and game_on: 
        mode = (mode + 1) % 3
        print(f"Switched to mode {mode} - {'Normal' if mode == 0 else 'Sneaking' if mode == 1 else 'Aggressive'}")

def move():
    global game_off_message_printed

    if not game_on:
        if not game_off_message_printed:
            print("The game is off. Can't move!")  
            game_off_message_printed = True 
        return

    game_off_message_printed = False 

    if joystick_x.is_pressed and not joystick_y.is_pressed:
        if mode == 0:
            print("Moving normally horizontally")
        elif mode == 1:
            print("Sneaking horizontally")
        elif mode == 2:
            print("Sprinting horizontally")
    elif joystick_y.is_pressed and not joystick_x.is_pressed:
        if mode == 0:
            print("Moving normally vertically")
        elif mode == 1:
            print("Sneaking vertically")
        elif mode == 2:
            print("Charging vertically")
    elif joystick_x.is_pressed and joystick_y.is_pressed:
        if mode == 0:
            print("Moving diagonally normally")
        elif mode == 1:
            print("Sneaking diagonally")
        elif mode == 2:
            print("Sprinting diagonally")

def attack():
    if not game_on:
        print("The game is off. Can't attack!")
        return 

    if mode == 0:
        print("Shooting!")
    elif mode == 1:
        print("Melee attack!")
    elif mode == 2:
        print("Special attack!")

def jump():
    if not game_on:
        print("The game is off. Can't jump!") 
        return  

    if mode == 0:
        print("Jumping!")
    elif mode == 1:
        print("Crouching!")
    elif mode == 2:
        print("Double Jumping!")

button.when_pressed = button_pressed  
button.when_released = button_released  
switch.when_pressed = attack  
joystick_button.when_pressed = jump  

while True:
    move()
    time.sleep(0.1) 

pause()
