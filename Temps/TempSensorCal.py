import subprocess
while True:
	temp = subprocess.Popen(["/home/pi/GCB/TempSensorCal.sh"], stdout=subprocess.PIPE, shell=True)
	output, err = temp.communicate()
	print output