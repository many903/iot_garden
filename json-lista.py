import json

Garden="""
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
            'humedad':humedad,
            'temperatura':temperatura,
            'luz':luz,
            'moisture':moisture,
        }
        }
    }"""

print (Garden)
#intento de combertir el json a lista
lista = json.loads(Garden)

print(lista)
