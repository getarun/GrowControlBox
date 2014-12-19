import time
import GPIO
import subprocess
from config import configSet, checkExist

#Initialize pins#
def initGCB():
	checkExist()
	GPIO.modePin(configSet('lightspin'), "out")
	GPIO.modePin(configSet('fanpin'), "out")
	GPIO.modePin(configSet('co2pin'), "out")
	GPIO.modePin(3, "out")
	GPIO.writePin(configSet('lightspin'), 0)
	GPIO.writePin(configSet('fanpin'), 0)
	GPIO.writePin(configSet('co2pin'), 1)
	GPIO.writePin(3, 1)

	
	subprocess.call(["sudo", "modprobe", "wire"])
	subprocess.call(["sudo", "modprobe", "w1-gpio"])
	subprocess.call(["sudo", "modprobe", "w1-therm"])
	
	#if int(time.strftime("%H")) > 20 or int(time.strftime("%H")) < 9:
	#	GPIO.writePin(pinConfig.lights, 1)
	#	GPIO.writePin(pinConfig.co2, 0)
	#else:
	#	GPIO.writePin(pinConfig.lights, 0)
	#	GPIO.writePin(pinConfig.co2, 1)
