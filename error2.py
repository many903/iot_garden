
import time
import datetime
import serial
import firebase
from dhtxx import DHT11
import RPi.GPIO as GPIO

# no se importa ninguna libreria de control de pines dado a que la biblioteca del DHT corrobora si esta
# importada diche libreria y si no la importa y establece el uso en el modo BMC

watered = False
    
def automate():
    #if the time is in between an interval of +- 15 mins, while the moisture level < thresh keep motor running, else turn off motor
    thresh = 30
    global watered
    print ("watered?", watered)
    time = datetime.datetime.now().strftime("%H:%M")
    print ("current time", time)
    if (((time > "19:45") and (time < "20:40")) or ((time > "3:45") and (time < "4:15"))):
        if not watered:
            while True:
                moisture = moisture_sensor

                if (moisture > thresh):
                    GPIO.output(31,False)
                    watered = True
                    break

                else:
                    GPIO.output(31,True)
    else:
        watered = False
        GPIO.output(31,False)

GPIO.setmode(GPIO.BMC)
dht_sensor = DHT(18)
motor = 17
moisture_sensor = serial.Serial('/dev/ttyUSB0',9600)
light = serial.Serial('/dev/ttyUSB1',9600)

GPIO.setup(motor, GPIO.OUT)
GPIO.setup(dht_sensor, GPIO.IN)

firebase = firebase.FirebaseApplication('https://data-base-iot-garden-default-rtdb.firebaseio.com/ ', None)

initTime = time.time()


while True:
    motor_state = firebase.get('/iot-garden-monitoring-system', 'motor_state')
    update = firebase.get('/iot-garden-monitoring-system', 'update')
    pi_state = firebase.get('/iot-garden-monitoring-system', 'pi_state')

    r=dht11.get(max_tries=10) # donde el dht guarda informacion

    print ("received data in ", int(time.time() - initTime), "seconds")
    initTime = time.time()

    if (pi_state == str("0")):
        GPIO.output(31,False)
        break
    temp = r[0]
    humidity = r[1]
    light = serial.Serial('/dev/ttyACM0',9600)
    moisture = serial.Serial('/dev/ttyACM1',9600)
    
    luz = light.readline()
    humedad_relativa = moisture.readline()

    print ("temp = ", temp)
    print ("humidity = ", humidity)
    print ("light = ", luz)
    print ("moisture = ", humedad_relativa)


    if (update == str("1")):
        print ("updating db")
        firebase.put('iot-garden-monitoring-system', 'temperature', str(temp))
        firebase.put('iot-garden-monitoring-system', 'humidity', str(humidity))
        firebase.put('iot-garden-monitoring-system', 'light', str(light))
        firebase.put('iot-garden-monitoring-system', 'moisture', str(moisture))
        firebase.put('iot-garden-monitoring-system', 'update', str(0))
        
    if (motor_state == str("1")):
        #turn on motor
        print ("motor turned on")
        GPIO.output(31,True)
    elif (motor_state == str("2")):
        #automate
        print ("motor automatic control")
        automate()
    else:
        #turn off motor
        print ("motor turned off")
        GPIO.output(31,False)