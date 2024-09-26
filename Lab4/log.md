Testing ESP32 board with Arduino
- ran blink

Finding MAC ADDRESS
- used code given in esp_mac_addr.ino
    - MAC ADDRESS: E8:68:E7:30:61:4C

Joystick:
- coded up the joystick
- analogRead used for analog
- must set the pin for digital read using pinMode(pin_num, INPUT_PULLUP)

Button:
- used Joystick code to configure the button

Switch:
- copied button code, it worked perfectly

Raspi and ESP32 communication:
- https://pythonhosted.org/pyserial/shortintro.html#readline
- used pyserial
- https://docs.espressif.com/projects/esp-idf/en/latest/esp32/get-started/establish-serial-connection.html
    - to find the port being used (ls /dev/tty*)