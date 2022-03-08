#include "DHT.h"  //libreria
#define DHTPIN 2  // Digital pin connected to the DHT sensor
#define DHTTYPE DHT11   // DHT 11
int luz = A0;
int moisture = A1;
int motor = 13; //Pin 13 para la bomba
char valor = '2';
DHT dht(DHTPIN, DHTTYPE);
int temp, humedad;//Configuro las variables de temperatura y humedad del DHT11

void setup() {
  Serial.begin(9600);
  Serial.println(F("DHTxx test!"));
  pinMode (luz, INPUT);
  pinMode (moisture, INPUT);
  pinMode (motor, OUTPUT);
  dht.begin();
}

void loop() {

  // put your main code here, to run repeatedly:
  int valor_analogico = analogRead(luz);
  int Valor_analogico = map(valor_analogico,0,1023,100,0);
  int sensorValue = analogRead(moisture); 
  int Value = map(sensorValue,0,1023,100,0);
  // Reading temperature or humidity takes about 250 milliseconds!
  // Sensor readings may also be up to 2 seconds 'old' (its a very slow sensor)
  int h = dht.readHumidity();
  // Read temperature as Celsius (the default)
  int t = dht.readTemperature();
  // Read temperature as Fahrenheit (isFahrenheit = true)
  int f = dht.readTemperature(true);

  // Check if any reads failed and exit early (to try again).
  if (isnan(h) || isnan(t) || isnan(f)) {
    Serial.println(F("Failed to read from DHT sensor!"));
    return;
  }

  // Compute heat index in Fahrenheit (the default)
  float hif = dht.computeHeatIndex(f, h);
  // Compute heat index in Celsius (isFahreheit = false)
  float hic = dht.computeHeatIndex(t, h, false);

  Serial.print(F(" "));
  Serial.print(h);
  Serial.print(F(" "));
  Serial.print(t);
  Serial.print(F(" "));
  Serial.print(Valor_analogico);
  Serial.print(F(" "));
  Serial.println(Value);
  
  
  humedad = h;
  temp = t;
  if (Serial.available ()>0) {//verificar si hay datos disponibles
    valor=Serial.read ();//leer los datos enviados
    if (valor=='1'){
       digitalWrite (motor, HIGH);
    }
    else if (valor=='2'){
       digitalWrite (motor, LOW);
    }
    else if (valor ='3') {
     if (sensorValue == 50){
        digitalWrite (motor, LOW);
     }
     else if (sensorValue >50){
        digitalWrite (motor, LOW);
     }
     else if( sensorValue < 50){
       digitalWrite (motor, HIGH);
     }
    }
    
  }

}
