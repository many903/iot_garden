int analogico = A0;

void setup() {
  // put your setup code here, to run once:
  pinMode (analogico, INPUT);
  Serial.begin(9600);

}

void loop() {
  // put your main code here, to run repeatedly:
  int valor_analogico = analogRead(analogico);
  int Valor_analogico = map(valor_analogico,0,1023,100,0);
  Serial.print(Valor_analogico);
  delay(1000);
}
