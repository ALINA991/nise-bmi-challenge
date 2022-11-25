#include <analogWrite.h>

int motorPin1 = 13;
const int dutyCycle = 1024;
float motor_wave = 0.05; // ranges from 0.05 to 1.0

void setup () {
  Serial.begin(512000);
  pinMode(motorPin1 , OUTPUT);
}
  
void loop() {
  if (motor_wave <= 1 && motor_wave >= 0) {
    analogWrite(motorPin1 , motor_wave * dutyCycle);
  }
  else {
    Serial.println("Warning:␣motor_wave␣must␣be␣smaller␣than␣1");
    }
  delay (500);
}
