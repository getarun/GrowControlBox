import xml.etree.ElementTree as ET
import os.path
import sys
from elementtree.ElementTree import ElementTree

configFileName = "GCBconfig.xml"


def checkExist():
	try:
		if os.path.exists(configFileName):
			return True
		else:
			buildDefaultXML()
			return True
	except:
		print('GCBconfig File Error!!')

def configSet (x):
	if checkExist()==True:
		tree = ET.parse(configFileName)
		root = tree.getroot()
		for e in root.getiterator():
			t = e.findtext(x)
			if t is not None:
				return t
		
		
def buildDefaultXML():
	configData = ET.Element('configData')
	
	#localization#
	localization = ET.SubElement(configData, 'localization')
	units = ET.SubElement(localization, 'units')
	temp = ET.SubElement(units, 'temp')
	temp.text = "F" ##Sets temp unit to F, all settings will need to reflect proper temps for selected unit of measurement.
	
	#pins XML Default Settings
	pins = ET.SubElement(configData, 'pins')
	lights = ET.SubElement(pins, 'lightspin')
	lights.text = "1" ##Lights Relay for GPIO pin (refer to Raspberry Pi pinout and GPIO standards for correct pin numbers) 
	fan = ET.SubElement(pins, 'fanpin')
	fan.text = "2" ##Fan Relay for GPIO pin (refer to Raspberry Pi pinout and GPIO standards for correct pin numbers) 
	co2 = ET.SubElement(pins, 'co2pin')
	co2.text = "3" ##CO2 Regulator Relay for GPIO pin (refer to Raspberry Pi pinout and GPIO standards for correct pin numbers) 

	
	#variables for airTemps, alarms, and such
	events = ET.SubElement(configData, 'events')
	exhaustTime = ET.SubElement(events, 'exhaustTime')
	exhaustTime.text = '15' ##Amount of time for the cycle  of the fan for stale air
	exhaustDuration = ET.SubElement(events, 'exhaustDuration')
	exhaustDuration.text = '2' ##Amount of time fan runs for exhausting

	airTemps = ET.SubElement(events, 'airTemps')
	hiTemp = ET.SubElement(airTemps, 'hiTemp')
	hiTemp.text = "78" ##Activate FAN for high temp
	lowTemp = ET.SubElement(airTemps, 'lowTemp')
	lowTemp.text = "76" ##Deactivate FAN for low temp
	hiTempAlarm = ET.SubElement(airTemps, 'hiTempAlarm')
	hiTempAlarm.text = "80" ##Alarm for too hot, not cooling down
	co2Event = ET.SubElement(events, 'CO2')
	co2Hi = ET.SubElement(co2Event, 'co2Hi')
	co2Hi.text = "1500" ##PPM of CO2 saturation high point shut off
	co2Low = ET.SubElement(co2Event, 'co2Low')
	co2Low.text = "1400" ##PPM of CO2 saturation low point activation 
	co2Alarm = ET.SubElement(co2Event, 'co2Alarm')
	co2Alarm.text = "600"
	
	APIkeys = ET.SubElement(configData, 'APIkeys')
	prowlkey = ET.SubElement(APIkeys, 'prowlkey')
	prowlkey.text = '6c3e99f97192f34dfc540b4412860c5047bba049' ##Prowl API Key for notifcations
	Xively = ET.SubElement(APIkeys, 'Xively')
	XivFeedID = ET.SubElement(Xively, 'XivFeedID')
	XivFeedID.text = '1689559581' ##Xively Feed ID
	XivAPIkey= ET.SubElement(Xively, 'XivAPIkey')
	XivAPIkey.text = 'KwFd4c3WbpRLCnmrB9iKbRZW3iGJWpHteCWp9NPqaCLMhGsJ' ##Xively API Key for datalogging
	
	tree = ET.ElementTree(configData)
	tree.write(configFileName)	


