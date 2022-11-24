#include <WiFi.h>
#include <WiFiUdp.h>

WiFiUDP Udp; // creation of wifi Udp instance 

char packetBuffer [255];

unsigned int localPort = 9999;

const char *ssid = "ESP32_for_IMU";
const char *password = "ICSESP32IMU";

void setup () {
  Serial.begin(512000);
  WiFi.softAP(ssid, password); // ESP32 as access point 
  Udp.begin(localPort);
}

void loop () {
  int packetSize = Udp.parsePacket(); 
  if (packetSize) {
    int len = Udp.read(packetBuffer , 255); 
    if (len > 0) packetBuffer[len-1] = 0;
    
    Serial.print("The␣receiving␣message␣is:␣");
    Serial.println(packetBuffer);
    delay (1000);
    }
}
 
