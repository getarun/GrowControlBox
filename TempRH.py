# Checks Temp/Humidity and returns values #
##############
import os
import subprocess
import GPIO #import GPIO functions
from config import configSet
import prowlpy
import time
import mysql.connector


###assign variables###
p = prowlpy.Prowl(configSet('prowlkey'))
DIR = '/sys/bus/w1/devices'
sensorlist = [name for name in os.listdir(DIR)]

def findTempSensors():
	'''Discovers sensors and prints the list'''
	for i in sensorlist:
		if not i.find('28-'):
			print i

def checkAirTemp(x=None):
	'''Returns the temp from desired sensor (or average the sensors)
	1 = Higher Sensor
	2 = Lower Sensor
	No values passed = Average the 2 sensors'''
	if x == 1:
		temp = subprocess.Popen(["Temps/AirTemp1.sh"], stdout=subprocess.PIPE, shell=True)
		output, err = temp.communicate() #converts output to string
		output = float(output) #converts string output to float output
	if x == 2:
		temp = subprocess.Popen(["Temps/AirTemp2.sh"], stdout=subprocess.PIPE, shell=True)
		output, err = temp.communicate() #converts output to string
		output = float(output) #converts string output to float output
	if x == None:
		temp1 = subprocess.Popen(["Temps/AirTemp1.sh"], stdout=subprocess.PIPE, shell=True)
		output1, err = temp1.communicate() #converts output to string
		output1 = float(output1) #converts string output to float output
		temp2 = subprocess.Popen(["Temps/AirTemp2.sh"], stdout=subprocess.PIPE, shell=True)
		output2, err = temp2.communicate() #converts output to string
		output2 = float(output2) #converts string output to float output
		output = (output1+output2)/2
	if configTempUnit == "F":	
		temp = (output/1000) * 1.8 + 32
	elif configTempUnit == "K":
		temp = (output/1000) + 273.15
	else:
		temp = (output/1000)
		
	return temp

def maintainAirTemp(temp=None, hotCondition=None, exhaustCondition=None, alarmCondition=None, timer=None):	
	'''
	This actually runs the program using the conditions set in GCBconfig.xml and based off the temp passed to the function.
	
	Proper use of this function--
	temp, airHotCondition, exhaustCondition, airAlarmCondition, airTimer = maintainAirTemp(airTemp, airHotCondition, exhaustCondition, airAlarmCondition, airTimer)
	'''
	## Temp/Hum ##
	
	if temp == None:
		print 'No temp variable being passed'
		return None
	if hotCondition == None or exhaustCondition == None or alarmCondition == None or timer == None:
		hotCondition = 0
		alarmCondition = 0
		timer = -1
		exhaustCondition = 0
	
	if temp > int(configHiTemp):
		GPIO.writePin(configSet('fanpin'), 1)
		hotCondition = 1
		timer = -1
	else:
		if temp < int(configLowTemp) and hotCondition == 1:
			GPIO.writePin(configSet('fanpin'), 1) #set this back to 0
			hotCondition = 0
			exhaustCondition = 0
			alarmCondition = 0
		if hotCondition == 1 : timer = -1
	if hotCondition == 0 and timer == -1:
		timer = time.time()
	else:
		if timer != -1 and time.time()-timer > (float(configExhaustTime)*60):
			GPIO.writePin(configSet('fanpin'), 1)
			exhaustCondition = 1
	if time.time()-timer > ((float(configExhaustTime)+float(configExhaustDuration))*60) and hotCondition == 0 and exhaustCondition == 1:
		timer = -1
		GPIO.writePin(configSet('fanpin'), 1) #set this back to 0
		exhaustCondition = 0
	
	if temp > int(configHiTempAlarm) and alarmCondition == 0:
		p.add('GCB', 'Air Temp is {:.4}'.format(str(temp))+configTempUnit, 'WARNING', 2)
		alarmCondition = 1
		
	if temp < int(configLowTemp) and alarmCondition == 1:
		p.add('GCB', 'Air Temp is {:.4}'.format(str(temp))+configTempUnit, 'Notification', 0)
		alarmCondition = 0
		
	return (temp, hotCondition, exhaustCondition, alarmCondition, timer)
	
	
	


	
def checkWaterTemp(x=None):
	

	## Get Temp, define how you want to take the reading. ##
	## 1: Left Temp Sensor                               ##
	## 2: Right Temp Sensor                               ##
	## None: Average between the 2 sensors.               ##
	if x == 1:
		temp = subprocess.Popen(["Temps/WaterTemp1.sh"], stdout=subprocess.PIPE, shell=True)
		output, err = temp.communicate() #converts output to string
		output = float(output) #converts string output to float output
	if x == 2:
		temp = subprocess.Popen(["Temps/WaterTemp2.sh"], stdout=subprocess.PIPE, shell=True)
		output, err = temp.communicate() #converts output to string
		output = float(output) #converts string output to float output
	if x == None:
		temp1 = subprocess.Popen(["Temps/WaterTemp1.sh"], stdout=subprocess.PIPE, shell=True)
		output1, err = temp1.communicate() #converts output to string
		output1 = float(output1) #converts string output to float output
		temp2 = subprocess.Popen(["Temps/WaterTemp2.sh"], stdout=subprocess.PIPE, shell=True)
		output2, err = temp2.communicate() #converts output to string
		output2 = float(output2) #converts string output to float output
		output = (output1+output2)/2
	if configTempUnit == "F":	
		temp = (output/1000) * 1.8 + 32
	elif configTempUnit == "K":
		temp = (output/1000) + 273.15
	else:
		temp = (output/1000)
	
	return temp
	
def WaterTempNotify(temp=None, waterAlarmCondition=None):
	## Water Temp ##
	##assign variables##
	if waterAlarmCondition==None:
		waterWarning = 0
	else:
		waterWarning = waterAlarmCondition
	
	if temp == None:
		print 'No temp variable being passed'
		return None
	if temp > 74 and waterWarning == 0:
		p.add('GCB', 'Warning: Water Temp is ' + str(temp) + 'F', 'WARNING', 2)
		waterWarning = 1
	if waterWarning == 1 and temp < 70:
		p.add('GCB', 'Water Temp is ' + str(temp) + 'F', 'Notification', 0)
		waterWarning = 0	

	return waterWarning
	
if __name__ == '__main__' :
	
	temp, airHotCondition, exhaustCondition, airAlarmCondition, airTimer, airTimeDisplay, waterAlarmCondition = None, None, None, None, None, None, None

	
	while True:
		try:
			cnx = mysql.connector.connect(user='GCB', database='GCB', password='GCB', host='192.168.2.2')
			cursor = cnx.cursor()
			sqlcondition = 1
		except:
			print "MySQL Connection Failed..."
			time.sleep(.5)
			sqlcondition = 0
		configHiTemp = configSet('hiTemp')
		configLowTemp = configSet('lowTemp')
		configHiTempAlarm = configSet('hiTempAlarm')
		configExhaustTime = configSet('exhaustTime')
		configExhaustDuration = configSet('exhaustDuration')
		configTempUnit = configSet('temp')
		airTemp1 = checkAirTemp(1)
		airTemp2 = checkAirTemp(2)
		airTemp = airTemp2
		waterTemp1 = checkWaterTemp(1)
		waterTemp2= checkWaterTemp(2)
		statusString = ''
		waterAlarmCondition = WaterTempNotify(waterTemp1, waterAlarmCondition)
		temp, airHotCondition, exhaustCondition, airAlarmCondition, airTimer = maintainAirTemp(airTemp, airHotCondition, exhaustCondition, airAlarmCondition, airTimer)
		if airTimer == -1:
			airTimeDisplay = 'FAN'
		else:
			if time.time()-airTimer > (float(configExhaustTime))*60 :
				airTimeDisplay = 'Exhausting for {:.4}'.format(str(((time.time()-airTimer)-((((float(configExhaustTime)+float(configExhaustDuration))*60))))))+' more seconds'
			else:
				statusString = statusString+'Timer running. Waiting for stale air or other condition.'
				airTimeDisplay = '{:.3}'.format(str(time.time()-airTimer))+' seconds'
		
		if airHotCondition == 1:
			statusString = statusString+'Air is hot, Fan ON'
		elif exhaustCondition == 1:
			statusString = statusString+'Stale Air, Fan ON'
		elif airAlarmCondition == 1:
			statusString = statusString+'Air is TOO HOT, Send WARNING Notification'

		
		os.system('clear')
		print '******Temp/Humidity Test******'
		print ''
		print '###Conditions###'
		print 'Air Temp (Maintained): {:.4}'.format(str(airTemp))+configTempUnit
		print 'Air Temp Upper: {:.4}'.format(str(airTemp1))+configTempUnit
		print 'Air Temp Lower: {:.4}'.format(str(airTemp2))+configTempUnit
		print 'airHotCondition: '+str(airHotCondition)
		print 'exhaustCondition: '+str(exhaustCondition)
		print 'airAlarmCondition: '+str(airAlarmCondition)
		print 'airTimer: '+str(airTimeDisplay)
		print 'Water Temp (Left): {:.4}'.format(str(waterTemp1))+configTempUnit
		print 'Water Temp (Right): {:.4}'.format(str(waterTemp2))+configTempUnit
		print ''
		print '###Settings###'
		print 'Air High Temp Setting: '+configHiTemp+configTempUnit
		print 'Air Low Temp Setting: '+configLowTemp+configTempUnit
		print 'Alarm Temp Setting: '+configHiTempAlarm+configTempUnit
		print 'Exhaust Time Setting: '+str(float(configExhaustTime)*60)+' seconds'
		print ''
		print '#####STATUS#####'
		print statusString

		if GPIO.readPin(1) == 0 and airHotCondition == 0 and exhaustCondition == 0:
			GPIO.writePin(2, 0)
		if sqlcondition != 0:
			try:
				sqlRecord = ("INSERT INTO rpi1(AirTemp1, AirTemp2, WaterTemp1, WaterTemp2, LightsState, LightCycle, FanState, Status) VALUES({:.4}".format(str(airTemp1))+", {:.4}".format(str(airTemp2))+", {:.4}".format(str(waterTemp1))+", {:.4}".format(str(waterTemp2))+", "+str(GPIO.readPin(configSet('lightspin')))+", 1212, "+str(GPIO.readPin(configSet('fanpin')))+", '"+statusString+"');")
				sqlCleanUp = ("DELETE FROM rpi1 WHERE time <= DATE_SUB(CURDATE(), INTERVAL 3 MONTH);")
				cursor.execute(sqlRecord)
				print "Inserted data into database..."
				cursor.execute(sqlCleanUp)
				print "Removed data older than 3 months from database..."
				cnx.commit()
			except:
				print "ERROR: Could not INSERT data into TABLE!!"
