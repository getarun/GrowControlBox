# This reads PPM, checks fan state, checks light state, and then supplements #
##############

#import GPIO #import GPIO functions
#import pinConfig #import pinConfig for device configuration
import prowlpy
import GPIO
import pinConfig
apikey = '6c3e99f97192f34dfc540b4412860c5047bba049' # Prowl apikey
p = prowlpy.Prowl(apikey)

def checkCO2():
	#ppm = GPIO.readPin(pinConfig.ppmMeter) #read PPM levels
	ppm = 1400
	return ppm

def supplementCO2():
	fanState = GPIO.readPin(pinConfig.fan) #get fan pin state
	lightState = GPIO.readPin(pinConfig.lights) #get lights pin state
	#ppm = GPIO.readPin(pinConfig.ppmMeter) #read PPM levels
	ppm = 1400
	supplementState = 0
	with open('tankStatus.txt', 'r') as tankFile:
		tank = int(tankFile.readline())
	if ppm < 1500 and fanState == 0 and lightState == 1 and tank == 1:
		GPIO.writePin(pinConfig.co2, 0)
		supplementState = 1
	else:
		GPIO.writePin(pinConfig.co2, 1)
		supplementState = 0
	return supplementState