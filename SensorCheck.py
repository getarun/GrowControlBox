import os

DIR = '/sys/bus/w1/devices'
sensorlist = [name for name in os.listdir(DIR)]

def findSensors():
	for i in sensorlist:
		if not i.find('28-'):
			print i
			
findSensors()