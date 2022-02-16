int sensorPin = A0; 
int sensorValue;  
int limit = 300; 

void setup() {
 Serial.begin(9600);
 pinMode(13, OUTPUT);
}

void loop() {

 sensorValue = analogRead(sensorPin); 
 int Value = map(sensorValue,0,1023,100,0);
 Serial.println(Value);

 
 delay(1000); 
}
