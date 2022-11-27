// Band pass butterworth filter order=2 alpha1=0.1 alpha2=0.49 
//https://vocal.com/resources/development/why-is-shifting-necessary-in-fixed-point-ffts/
// Thien's COMP6
#include <Adafruit_LSM6DSOX.h>
#include <Adafruit_LIS3MDL.h>
#include <Wire.h>


// DEFINE PINS 
#define analogInPin 26 // Analog Pin A0; 
#define I2C_SDA 23
#define I2C_SCL 22
const int bufferSize = 150; // 150  RMS buffer size

class filter
{
  public:
    filter()
    {
      for(int i=0; i <= 4; i++)
        v[i]=0;
    }
  private:
    short v[5];
    short step(short x)
    {
      v[0] = v[1];
      v[1] = v[2];
      v[2] = v[3];
      v[3] = v[4];
      // The long number is devided by 1 or 2 then the whole thing is divided by 2^19 
      // or 524288
      long tmp = ((((x * 640414L) >>  1)  // = (   6.1074604183e-1 * x)
        + ((v[0] * -794022L) >> 2)  // +( -0.3786192994*v[0])
        + ((v[1] * 526823L) >> 2) // +(  0.2512087022*v[1])
        + ((v[2] * 888806L) >> 1) // +(  0.8476319007*v[2])
        + ((v[3] * -809871L) >> 1)  // +( -0.7723536365*v[3])
        )+262144) >> 19; // round and downshift fixed point /524288

      v[4]= (short)tmp;
      return (short)((
         (v[0] + v[4])
        - 2 * v[2])); // 2^
    }
};

////// CLASS IMU 
class IMU 
{
  public:
    // IMU()
    // {

    // }
    Adafruit_LSM6DSOX lsm6dsox;
    Adafruit_LIS3MDL lis3mdl;
    sensors_event_t accel;
    sensors_event_t gyro;
    sensors_event_t mag;
    sensors_event_t temp;

    void init(){
      if (!lsm6dsox.begin_I2C ()) {
      Serial.println (" Failed to find LSM6DSOX chip ");
      while (1) {delay (10);}
      }
      if (!lis3mdl.begin_I2C ()) {
      Serial.println (" Failed to find LIS3MDL chip ");
      while (1) {delay (10);}
      }
      Serial.println("Connected!!!!!");
    }

    void  get_sensor_events(){
      lsm6dsox.getEvent (&accel , &gyro , &temp );
      lis3mdl.getEvent (&mag );
    }

    int * get_gyroscope_data(){
      static int g[3];
      g[0] = gyro.gyro.x;
      g[1] = gyro.gyro.y;
      g[2] = gyro.gyro.z;
      //  accel . acceleration .x
      // mag. magnetic .x
      return g;
    }



  private:

};

Adafruit_LSM6DSOX lsm6dsox;
Adafruit_LIS3MDL lis3mdl;
sensors_event_t accel;
sensors_event_t gyro;
sensors_event_t mag;
sensors_event_t temp;

int sensorValue = 0;       

int rmsBuffer[bufferSize];
double rmsValue;
double msTemp;
int bufferCounter;
double roll;
double pitch;

// IMU 
//IMU imu;

int *gyro_data;
int *acc_data;
int *mag_data; 

void setup() {
  // EMG
  initBuffer();
  bufferCounter = 0;
  rmsValue = 0.0;
  msTemp = 0.0;
  // IMU
  Wire.begin ( I2C_SDA , I2C_SCL );
  //imu.init();
  Serial.begin(500000);
    if (!lsm6dsox.begin_I2C ()) {
  Serial.println (" Failed to find LSM6DSOX chip ");
  while (1) {delay (10);}
  }
  if (!lis3mdl.begin_I2C ()) {
  Serial.println (" Failed to find LIS3MDL chip ");
  while (1) {delay (10);}
  }
  Serial.println("Connected!!!!!");
  
  delay(1000);
}

void loop() {
      sensorValue = analogRead(analogInPin) - 1800; // -1800;
      rmsValue = calculateRMS(rmsBuffer, sensorValue);
      //imu.get_sensor_events();
      //imu.get_gyroscope_data(gyro_data);
      //Serial.println(gyro_data + 1);
  //    Serial.println(rmsValue);
      lsm6dsox.getEvent (&accel , &gyro , &temp );
      lis3mdl.getEvent (&mag);
      sensors_event_t accel;
      sensors_event_t gyro;
      sensors_event_t mag;
      sensors_event_t temp; lsm6dsox.getEvent(&accel, &gyro, &temp); lis3mdl.getEvent(&mag);
      // pitch
      pitch = atan2(accel.acceleration.y, sqrt(accel.acceleration.x*accel.acceleration.x + accel.acceleration.z*accel.acceleration.z))*RAD_TO_DEG; // roll
      roll = atan2(-accel.acceleration.x, sqrt(accel.acceleration.y*accel.acceleration.y + accel.acceleration.z*accel.acceleration.z))*RAD_TO_DEG;
        /* Display the results (pitch roll) */

  
      Serial.print(gyro.gyro.x); 
      Serial.print("\t");

      Serial.print(gyro.gyro.y); 
      Serial.print("\t");
      
      Serial.print(gyro.gyro.z); 
      Serial.print("\t");


      Serial.print(accel.acceleration.x); // push (1 negative, 2 pos) and pull (1 pos, 2 neg)
      Serial.print("\t");

      Serial.print(accel.acceleration.y); 
      Serial.print("\t");
      
      Serial.print(accel.acceleration.z); 
      Serial.print("\t");

      Serial.print(mag.magnetic.x); 
      Serial.print("\t");

      Serial.print(mag.magnetic.y); 
      Serial.print("\t");
      
      Serial.print(mag.magnetic.z); 
      Serial.print("\t");

      Serial.print(pitch); // positive left, negative right
      Serial.print("\t");   
      
      Serial.print(roll);  //up negative, back positive 
      Serial.print("\t");

      Serial.print(rmsValue);

//            Serial.print("\t");
//      Serial.print(45);
//      Serial.print("\t");
//      Serial.print(-45);
//      Serial.print("\t");
      Serial.print("\n");

      

      
  delay (1); 
}

void initBuffer(){
  for (int i = 0; i < bufferSize; i++){
    rmsBuffer[i] = 0;
  }
}

double calculateRMS(int buff[bufferSize], int value){
  

  rmsBuffer[bufferCounter] = sensorValue;
  double rmstemp = 0.0;
  for (int i =0; i <bufferSize; i++){
    rmstemp = rmstemp + float(rmsBuffer[i])*rmsBuffer[i];
  }
  
  if (bufferCounter >= bufferSize-1){
    bufferCounter = 0;
  }
  else{
    bufferCounter++;
  }

  return sqrt(rmstemp/bufferSize);

}
