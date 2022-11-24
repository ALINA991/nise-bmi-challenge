int motorPin1 = 13;   // GPIO 13 for vibration motor 1
int motorPin2 = 12;  // GPIO 12 for vibration motor 2
void setup()
{
  pinMode(motorPin1, OUTPUT);
  pinMode(motorPin2, OUTPUT);
}

void loop ()
{
  digitalWrite(motorPin1, HIGH);
  digitalWrite(motorPin2, HIGH);
  delay(1000);
  digitalWrite(motorPin1, LOW);
  digitalWrite(motorPin2, LOW);
  delay (1000);
}
