#librerias
import firebase_admin #pip install firebase_admin
import time
import datetime
import serial
from dhtxx import DHT11 # git clone https://github.com/jdupl/dhtxx-rpi-python3
import RPi.GPIO as GPIO
from firebase_admin import db
from firebase_admin import credentials

#pines
GPIO.setmode(GPIO.BMC)
dht_sensor = DHT(18)
motor = 17
moisture_sensor = serial.Serial('/dev/ttyUSB0',9600)
light = serial.Serial('/dev/ttyUSB1',9600)

# modo
GPIO.setmode(GPIO.BMC)

# funcion aturomatico
def automatico():
    suelo = 50
    moisture = moisture_sensor
    moisture= moisture.decode('utf8').strip()
    moisture = moisture.readline()
    if (moisture < suelo):
        GPIO.output(31,True)
    else:
        GPIO.output(31,False)

#credenciales para mover la base de datos
cred = credentials.Certificate("path/to/serviceAccountKey.json")
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
            }
            'raspberrypi':
            {
                'humedad':humedad,
                'temperatura':temperatura,
                'luz':luz,
                'moisture':moisture,
            }
        }
})


while True:
    r=dht_sensor.get_reults(max_tries=10)
    
    #lectura de los registros de luz
    luz= luz.decode('utf8').strip()
    luz= light.readline()
    print('luz:'luz )

    # lectura del valor de humedad relativa
    moisture = moisture_sensor
    moisture = moisture.decode('utf8').strip()
    moisture = moisture.readline()
    # lectura del valor del dht_sensor
    if r:
        temperatura = r[0]
        humedad = r[1]

    #lectura de datos
    app_ref = ref.child('app')
    update = app_ref.order_by('update').limit_to_last(1).get()
    motor_state = app_ref.order_by('motor_state').limit_to_last(1).get()
    pi_state = app_ref.order_by('pi_state').limit_to_last(1).get()

    #actualizacion de datos (push)
    ref = db.reference('Garden')
    rasp_ref = ref.child('raspberrypi')
    
    if (update == '1'):
        self.ref.child("garden").child(rasp_ref).setValue(["humedad": str(humedad)])
        self.ref.child("garden").child(rasp_ref).setValue(["temperatura": str(temperatura)])
        self.ref.child("garden").child(rasp_ref).setValue(["luz": str(luz)])
        self.ref.child("garden").child(rasp_ref).setValue(["moisture": str(moisture)])

    print(update)
    print(motor_state)
    print(pi_state)

    if (motor_state == 0)
        GPIO.output(motor, False)
    elif(motor_state == 1)
        GPIO.output(motor, True)
    else:
        automatico() 