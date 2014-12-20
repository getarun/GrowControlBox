import subprocess

def readPin(n): #function for reading GPIO pins
	n = str(n) #take int value and convert to string
	pinState = subprocess.Popen(["gpio read " + n], stdout=subprocess.PIPE, shell=True) #read pin state and PIPE
	output, err = pinState.communicate() #converts output to string
	output = int(output) #converts string output to int output
	return output

def writePin(n, s): #function for writing GPIO pins
	n = str(n) #take int value and convert to string
	s = str(s) #take int value and convert to string
	writePn = subprocess.call(["gpio", "write", n, s]) #write pin, and its state
	
def modePin(n, s): #function for writing GPIO pins
	n = str(n) #take int value and convert to string
	s = str(s) #take int value and convert to string
	writePn = subprocess.call(["gpio", "mode", n, s]) #write pin, and its state