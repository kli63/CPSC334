import serial

while True:
    ser = serial.Serial('/dev/ttyUSB0', 115200, 8, 'N', 1, timeout=0.1)
    output1 = ser.readline().decode("utf-8")
    output2 = ser.readline().decode("utf-8")
    output3 = ser.readline().decode("utf-8")
    output4 = ser.readline().decode("utf-8")
    output5 = ser.readline().decode("utf-8")
    print(output1 + output2 + output3 + output4 + output5)
   