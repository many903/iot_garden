#librerias
import firebase_admin #pip install firebase_admin
import time
import datetime
import serial
from dhtxx import DHT11,DHT # git clone https://github.com/jdupl/dhtxx-rpi-python3
import RPi.GPIO as GPIO
from firebase_admin import db
from firebase_admin import credentials

#pines
dht_sensor = DHT(18)
motor = 17
moisture_sensor = serial.Serial('/dev/ttyUSB0',9600)
light = serial.Serial('/dev/ttyUSB1',9600)

# modo
GPIO.setmode(GPIO.BCM)

# funcion aturomatico
def automatico():
   suelo = 50
   humedad_suelo = serial.Serial('/dev/ttyUSB0',9600)
   if (humedad_suelo < suelo):
        GPIO.output(31,True)
   else:
        GPIO.output(31,False)

#credenciales para mover la base de datos
cred = credentials.Certificate("/home/pi/Desktop/iot-garden-92204-firebase-adminsdk-a723z-2d3767458f.json")
firebase_admin.initialize_app(cred,{

    'databaseURL':'https://iot-garden-92204-default-rtdb.firebaseio.com/'

})
# como se va a estructurar la base de datos
ref = db.reference('/')
ref.set({
    'Garden': 
        {
            'app':
            {
                'update': 1, 
                'pi_state':1,
                'motor_state':0
            },
            'raspberrypi':
            {
                'humedad':0,
                'temperatura':0,
                'luz':0,
                'moisture':0,
            },
        }
})


while True:
    r = dht_sensor.get_result(max_tries=10)
    humedad = 0
    temperatura =0
    if r == None:
        r = dht_sensor.get_result(max_tries = 10 )
        if r:
            print('Temp: {0:0.1f} C Humidity; {1:0.1f} %'.format(r[0], r[1]))
            temperatura = r[0]
            humedad = r[1]
    luz = light.readline()
    luz = luz.decode('utf8').strip()
    print ( 'luz:',luz )
    moisture = moisture_sensor
    moisture = moisture.readline()
    moisture = moisture.decode('utf8').strip()
    print ( 'moisture:',moisture )
    #actualizacion de datos (push)
    ref = db.reference('Garden')
    rasp_ref = ref.child('raspberrypi')
    luz = int(luz)
    humedad = int(humedad)
    moisture = int(moisture)
    temperatura = int(temperatura)
    rasp_ref.update({
            'humedad':humedad,
            'temperatura': temperatura,
            'luz':luz,
            'moisture':moisture_sensor
    })
    #lectura de datos
    app_ref = ref.child('app')
    update = app_ref.order_by('update').limit_to_last(1).get()
    motor_state = app_ref.order_by('motor_state').limit_to_last(1).get()
    pi_state = app_ref.order_by('pi_state').limit_to_last(1).get()

    print(update)
    print(motor_state)
    print(pi_state)

    if (motor_state == 0):
        GPIO.output(motor, False)
    elif(motor_state == 1):
        GPIO.output(motor, True)
    else:
        automatico()