// Band pass butterworth filter order=2 alpha1=0.1 alpha2=0.49 
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

const int analogInPin = 26; // Analog Pin A0; 

int sensorValue = 0;       

const int bufferSize = 150; // 150
int rmsBuffer[bufferSize];
double rmsValue;
double msTemp;
int bufferCounter;


void setup() {
  initBuffer();
  bufferCounter = 0;
  rmsValue = 0.0;
  msTemp = 0.0;
  Serial.begin(512000);
  delay(1000);
}

void loop() {
    sensorValue = analogRead(analogInPin) - 1800; // -1800;
    rmsValue = calculateRMS(rmsBuffer, sensorValue);
    Serial.println(rmsValue);
    
    delay(20);
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
