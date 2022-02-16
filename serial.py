from uu import decode
import serial
ser=serial.Serial('/dev/ttyACM0',9600)
#ser=ser.decode('utf8').strip()
readedText = ser.readline()
print(readedText)
ser.close()