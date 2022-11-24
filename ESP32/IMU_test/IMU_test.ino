// Basic demo for accelerometer & gyro & compass readings from Adafruit 
// LSM6DSOX and LIS3MDL sensor
#include <Wire.h>
#include <Adafruit_LSM6DSOX.h>
#include <Adafruit_LIS3MDL.h>

// I2C pins
#define I2C_SDA 23 
#define I2C_SCL 22

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
  
  Serial.print("\t\tTemperature␣");
  Serial.print(temp.temperature);
  Serial.println("␣deg␣C");
  
  /* Display the results (acceleration is measured in m/s^2) */
  Serial.print("\t\tAccel␣X:␣");
  Serial.print(accel.acceleration.x);
  Serial.print("␣\tY:␣");
  Serial.print(accel.acceleration.y);
  Serial.print("␣\tZ:␣");
  Serial.print(accel.acceleration.z);
  Serial.println("␣m/s^2␣");
  /* Display the results (rotation is measured in rad/s) */
  Serial.print("\t\tGyro␣X:␣");
  Serial.print(gyro.gyro.x);
  Serial.print("␣\tY:␣");
  Serial.print(gyro.gyro.y);
  Serial.print("␣\tZ:␣");
  Serial.print(gyro.gyro.z);
  Serial.println("␣radians/s␣");
  /* Display the results (magnetic field is measured in uTesla) */
  Serial.print("␣\t\tMag␣X:␣");
  Serial.print(mag.magnetic.x);
  Serial.print("␣\tY:␣");
  Serial.print(mag.magnetic.y);
  Serial.print("␣\tZ:␣");
  Serial.print(mag.magnetic.z);
  Serial.println("␣uTesla␣");
  Serial.println();
  
  delay (100);
}


 
