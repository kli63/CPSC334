from gpiozero import Button

button = Button(2)
switch = Button(3)

joystick_1 = Button(14)
joystick_2 = Button(15)
joystick_3 = Button(18)

gameOn = switch.is_pressed

switch.wait_for_press()
print("Starting game!")

while True:
    if gameOn:
        print("hi")