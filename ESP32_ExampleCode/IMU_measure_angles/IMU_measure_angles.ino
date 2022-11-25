// Basic demo for pitch and roll readings from Adafruit 
// LSM6DSOX and LIS3MDL sensor
#include <Wire.h>
#include <Adafruit_LSM6DSOX.h>
#include <Adafruit_LIS3MDL.h>

// I2C pins
#define I2C_SDA 23 
#define I2C_SCL 22

// for angle calculations
#define PI 3.1415926535897932384626433832795
#define RAD_TO_DEG 57.295779513082320876798154814105

double roll; 
double pitch;

Adafruit_LSM6DSOX lsm6dsox; 
Adafruit_LIS3MDL lis3mdl; 

void setup(void) {
  Wire.begin(I2C_SDA, I2C_SCL);
  Serial.begin(512000);
  while (!Serial)
    delay (10);
    
  Serial.println("Adafruit␣LSM6DSOX+LIS3MDL␣test!");
  
// Try to intialize!
if (!lsm6dsox.begin_I2C()) {
  Serial.println("Failed␣to␣find␣LSM6DSOX␣chip");
  while (1) {
    delay (10);
    }
  }
  if (!lis3mdl.begin_I2C()) {
    Serial.println("Failed␣to␣find␣LIS3MDL␣chip");
    while (1) {
      delay (10);
      }
    }
    
    Serial.println("LSM6DSOX␣and␣LIS3MDL␣Found!");
}



void loop () {
  
  // /* Get a new normalized sensor event */
  sensors_event_t accel;
  sensors_event_t gyro;
  sensors_event_t mag;
  sensors_event_t temp;
  lsm6dsox.getEvent(&accel, &gyro, &temp);
  lis3mdl.getEvent(&mag);
    // pitch
  pitch = atan2(accel.acceleration.y,
  sqrt(accel.acceleration.x*accel.acceleration.x + 
  accel.acceleration.z*accel.acceleration.z))*RAD_TO_DEG;
  // roll
  roll = atan2(-accel.acceleration.x, 
  sqrt(accel.acceleration.y*accel.acceleration.y + 
  accel.acceleration.z*accel.acceleration.z))*RAD_TO_DEG;
  
  /* Display the results (pitch roll) */
  Serial.print("␣Pitch:␣");
  Serial.print(pitch);
  Serial.print("␣Roll:␣");
  Serial.print(roll);
  Serial.println("␣degree␣");
  Serial.println();
  
  delay (100);
}
 
