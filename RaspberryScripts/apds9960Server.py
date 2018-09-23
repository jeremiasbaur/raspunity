from apds9960.const import *
from apds9960 import APDS9960
import RPi.GPIO as GPIO
import smbus, socket
from time import sleep

# APDS9960 Setup
portSensor = 1
bus = smbus.SMBus(portSensor)

apds = APDS9960(bus)

def intH(channel):
	print("INTERRUPT")

GPIO.setmode(GPIO.BOARD)
GPIO.setup(7, GPIO.IN)

# Server Setup
host, port = '192.168.7.153', 2121 # enter ipv4 address of pc which is in the same network
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
	s.bind((host, port))
except:
	print("Failed to bind")

s.listen(5)
print("Waiting for data")

(conn, addr) = s.accept()
print("Connected")

#try:
# Interrupt-Event hinzufuegen, steigende Flanke
GPIO.add_event_detect(7, GPIO.FALLING, callback = intH)

apds.setProximityIntLowThreshold(50)

print("Light Sensor Test")
print("=================")
apds.enableLightSensor()
apds.enableProximitySensor()
ovalLight = -1
ovalProx = -1
while True:
	sleep(0.03) # if it's too low, unity can't handle it (weird)
	valLight = apds.readAmbientLight()
	valProx = apds.readProximity()
	if valLight != ovalLight:
		print("AmbientLight={}".format(valLight))
		ovalLight = valLight
	if valProx != ovalProx:
		print("proximity={}".format(valProx))
		ovalProx = valProx
	#data = conn.recv(1024)
	#print("Received:", data.decode('utf-8'))
	reply = "1,1,"+str(255-valProx)+","
	conn.send(reply.encode('utf-8'))

#finally:
GPIO.cleanup()
print("Bye")
conn.close()
