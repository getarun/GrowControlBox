import subprocess
import time
import prowlpy
import GPIO
from config import configSet
from initialize import initGCB
from TempRH import checkAirTemp, checkWaterTemp

###assign variables###
p = prowlpy.Prowl(configSet('prowlkey'))
waterWarning = 0
CO2timer = -1
FANtimer = -1
exhaust = 0
AirHot = 0
tempAlarm = 0
#################

initGCB()

#main script
while True:
	## Temp/Hum ##
	if checkAirTemp() > int(configSet('hiTemp')):
		GPIO.writePin(configSet('fanpin'), 1)
		AirHot = 1
		FANtimer = -1
	else:
		if exhaust != 1 and checkAirTemp() < int(configSet('lowTemp')) and AirHot == 1:
			GPIO.writePin(configSet('fanpin'), 0)
			AirHot = 0
			tempAlarm = 0
	
	if AirHot == 0 and FANtimer == -1:
		FANtimer = time.time()
	else:
		if FANtimer != -1 and time.time()-FANtimer > int(configSet('exhaustTime'))*60:
			GPIO.writePin(configSet('fanpin'), 1)
			exhaust = 1
	if time.time()-FANtimer > (int(configSet('exhaustTime'))+2)*60 and AirHot == 0:
		FANtimer = -1
		GPIO.writePin(configSet('fanpin'), 0)
		exhaust = 0
	
	if checkAirTemp() > int(configSet('hiTempAlarm')) and tempAlarm == 0:
		p.add('GCB', 'Air Temp is {:.4}'.format(checkAirTemp())+configSet('temp'), 'WARNING', 2)
		tempAlarm = 1
		
	if checkAirTemp() < int(configSet('lowTemp')) and tempAlarm == 1:
		p.add('GCB', 'Air Temp is {:.4}'.format(checkAirTemp())+configSet('temp'), 'Notification', 0)
		tempAlarm = 0
	
	if GPIO.readPin(configSet('lightspin')) == 1 and tank == 1:
		if GPIO.readPin(configSet('fanpin')) == 1:
			GPIO.writePin(configSet('co2pin'), 1)
		if GPIO.readPin(configSet('fanpin')) == 0:
			GPIO.writePin(configSet('co2pin'), 0)
	else:
		GPIO.writePin(configSet('co2pin'), 1)

	## Water Temp ##
	waterTemp = checkWaterTemp()
	print checkWaterTemp(1)
	print checkWaterTemp(2)
	print waterTemp
	if waterTemp > 79 and waterWarning == 0:
		waterTemp = str(waterTemp)
		p.add('GCB', 'Warning: Water Temp is ' + waterTemp + 'F', 'WARNING', 2)
		waterWarning = 1
	if waterWarning == 1 and waterTemp < 70:
		waterTemp = str(waterTemp)
		p.add('GCB', 'Water Temp is ' + waterTemp + 'F', 'Notification', 0)
		waterWarning = 0		

	time.sleep(1)