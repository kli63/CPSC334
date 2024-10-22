#include <WiFi.h>
#define LIGHT_SENSOR_PIN 34

const char* ssid = "yale wireless";
const char* server_ip = "172.29.31.198";
const int server_port = 10000;

void setup() {
  analogSetAttenuation(ADC_11db);
  Serial.begin(115200);

  WiFi.begin(ssid);
  unsigned long startAttemptTime = millis();
  const unsigned long timeout = 10000;

  while (WiFi.status() != WL_CONNECTED && millis() - startAttemptTime < timeout) {
    delay(500);
    Serial.println("...");
  }

  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("Failed to connect to WiFi");
    return;
  }

  Serial.print("WiFi connected with IP: ");
  Serial.println(WiFi.localIP());
}

void loop() {
  WiFiClient client;
  if (!client.connect(server_ip, server_port)) {
    Serial.println("Connection to host failed");
    delay(1000);
    return;
  }

  int analogValue = analogRead(LIGHT_SENSOR_PIN);
  String message = String(analogValue);

  client.print(message); 
  client.stop();

  Serial.print("Sent analog value: ");
  Serial.println(analogValue);

  delay(500);
}
