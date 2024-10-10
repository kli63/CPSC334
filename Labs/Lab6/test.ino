#include <WiFi.h>
#define LIGHT_SENSOR_PIN 34


const char* ssid = "yale wireless";

void setup() {
  analogSetAttenuation(ADC_11db);

  Serial.begin(115200);

  unsigned long startAttemptTime = millis();
  const unsigned long timeout = 10000;  // 10 seconds timeout   

  WiFi.begin(ssid);

  while (WiFi.status() != WL_CONNECTED && millis() - startAttemptTime < timeout) {
    delay(500);
    Serial.println("...");
  }

  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("Failed to connect to WiFi");
    return;  // Exit setup if WiFi connection failed
  }

  Serial.print("WiFi connected with IP:");
  Serial.println(WiFi.localIP());
}

void loop() {
//   WiFiClient client;
//   // if(!client.connect(IPAddress('192.168.0.130'), 3131)){  // <<< wrong!!
//    if(!client.connect(IPAddress("10.67.70.150"), 10000)){      // <<<<<< fixed
//  // if (!client.connect("192.168.1.68", 10000)) {            // <<< or like this
//     Serial.println("Connection to host failed");
//     delay(1000);
//     return;
//   }
//   Serial.println("client connected sending packet");    // <<< added
//   client.print("Hello from ESP32!");
//   client.stop();
  int analogValue = analogRead(LIGHT_SENSOR_PIN);

  Serial.print("Analog Value = ");
  Serial.print(analogValue);  

  if (analogValue < 40) {
    Serial.println(" => Dark");
  } else if (analogValue < 800) {
    Serial.println(" => Dim");
  } else if (analogValue < 2000) {
    Serial.println(" => Light");
  } else if (analogValue < 3200) {
    Serial.println(" => Bright");
  } else {
    Serial.println(" => Very bright");
  }

  delay(500);
}