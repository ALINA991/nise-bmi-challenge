int motorPin1 = 13; // GPIO 13 for vibration motor 1 
void setup ()
{
  pinMode(motorPin1, OUTPUT);   // pin configuration
}

void loop ()
{
  digitalWrite(motorPin1, HIGH);
  delay (1000);
  digitalWrite(motorPin1, LOW);
  delay (1000);
}
