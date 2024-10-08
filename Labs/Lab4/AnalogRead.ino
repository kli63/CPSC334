int x_pin = 34;
int y_pin = 35;
int joy_butt_pin = 15;
// int butt_pin = 16;

void setup() {
  // initialize serial communication at 115200 bits per second:
  Serial.begin(115200);

  //set the resolution to 12 bits (0-4095)
  analogReadResolution(12);
  pinMode(joy_butt_pin, INPUT_PULLUP);
  // pinMode(butt_pin, INPUT_PULLUP);



}

void loop() {
  // read the analog / millivolts value for pin 2:
  int analogValueX = analogRead(x_pin);
  int analogValueY = analogRead(y_pin);
  int analogVolts = analogReadMilliVolts(2);

  int joy_butt = digitalRead(joy_butt_pin);
  // int butt = digitalRead(butt_pin);


  // print out the values you read:
  Serial.printf("ADC analog x value = %d\n", analogValueX);
  Serial.printf("ADC analog y value = %d\n", analogValueY);
  Serial.printf("ADC analog joy_butt value = %d\n", joy_butt);
    // Serial.printf("ADC analog joy_butt value = %d\n", butt);



  // Serial.printf("ADC millivolts value = %d\n", analogVolts);

  delay(100);  // delay in between reads for clear read from serial
}
