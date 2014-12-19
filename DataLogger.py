#!/usr/bin/env python

import os
import xively
import subprocess
import time
import datetime
import requests
import GPIO
import pinConfig
import Setup

# initialize api client
api = xively.XivelyAPIClient(Setup.XivAPIkey)

# function to read the temperature from ds18b20 temperature sensor on i2c 
def read_temperatureAirTemp():
	temp = subprocess.Popen(["./checkAirTemp.sh"], stdout=subprocess.PIPE, shell=True)
	output, err = temp.communicate() #converts output to string
	output = float(output) #converts string output to float output
	temp = (output/1000) * 1.8 + 32
	temp = str("{:.4}".format(temp))
	return temp

# function to return a datastream object. This either creates a new datastream,
# or returns an existing one
def get_datastreamAirTemp(feed):
  try:
    datastream = feed.datastreams.get("AirTemp")
    return datastream
  except:
    datastream = feed.datastreams.create("AirTemp", tags="Temperature")
    return datastream

def get_datastreamLights(feed):
  try:
    datastream = feed.datastreams.get("Lights")
    return datastream
  except:
    datastream = feed.datastreams.create("Lights", tags="On/Off")
    return datastream
	
# main program entry point - runs continuously updating our datastream with the
# latest temperature reading
def run():
  feed = api.feeds.get(Setup.XivFeedID)

  datastreamAirTemp = get_datastreamAirTemp(feed)
  datastreamAirTemp.max_value = None
  datastreamAirTemp.min_value = None
  datastreamLights = get_datastreamLights(feed)
  datastreamLights.max_value = 1
  datastreamLights.min_value = 0

  while True:
	degreesFahrenheit = read_temperatureAirTemp()
	datastreamAirTemp.current_value = degreesFahrenheit
	datastreamAirTemp.at = datetime.datetime.utcnow()
	datastreamLights.current_value = GPIO.readPin(pinConfig.lights)
	datastreamLights.at = datetime.datetime.utcnow()
	try:
		datastreamAirTemp.update()
		datastreamLights.update()
	except requests.HTTPError as e:
		print "HTTPError({0}): {1}".format(e.errno, e.strerror)

	time.sleep(10)

run()
