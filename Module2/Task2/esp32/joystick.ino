const int joystickXPin = 34;
const int joystickYPin = 35;

void setup() {
  Serial.begin(115200);

  pinMode(joystickXPin, INPUT);
  pinMode(joystickYPin, INPUT);
}

void loop() {
  int joystickX = analogRead(joystickXPin);
  int joystickY = analogRead(joystickYPin);

  Serial.print("X:");
  Serial.print(joystickX);
  Serial.print(",Y:");
  Serial.println(joystickY);

  delay(100);
}
