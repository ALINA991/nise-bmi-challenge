#include <WiFi.h>
#include <WiFiUdp.h>

WiFiUDP Udp; // creation of wifi Udp instance 
char packetBuffer [255];
#define BUFFER_SIZE 500

unsigned int localPort = 9999;

const char *ssid = "ESP32_for_IMU";
const char *password = "ICSESP32IMU";

// declaration of default IP for server
IPAddress ipServidor(192, 168, 4, 1);
/*
* The ip address of the client has to be different to the server
* otherwise it will conflict because the client tries to connect
* to itself. */

IPAddress ipCliente(192, 168, 4, 10);  // different IP than server
IPAddress Subnet(255, 255, 255, 0);


void setup () {
  Serial.begin(512000);
  WiFi.begin(ssid, password);
  WiFi.mode(WIFI_STA); // ESP-32 as client
  WiFi.config(ipCliente , ipServidor , Subnet);
  Udp.begin(localPort);
}

void loop () {
  
// SENDING
Udp.beginPacket(ipServidor ,9999); // initiate transmission of data
char buf[BUFFER_SIZE]; // buffer to hold the string to append 
// appending to create a char
sprintf(buf, "Neuro-inspired␣Systems␣Engineering␣");
Udp.printf(buf); // print the char

Udp.printf("\r\n"); // end segment 

Udp.endPacket(); // close communication

Serial.print("The␣sending␣message␣is:␣");
Serial.println(buf);

delay (2000); 
}
 
