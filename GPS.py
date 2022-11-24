import serial
import time
import string
import pynmea2
import re

while True:
	port="/dev/ttyUSB0"
	ser=serial.Serial(port, baudrate=9600, timeout=0.5)
#	ser = serial.Serial("/dev/ttyUSB0", baudrate=115200, timeout=1)
	dataout = pynmea2.NMEAStreamReader()
	newdata=ser.readline()
	print(newdata)
#	print(dataout)
# 	time.sleep(1)

	if '$GNRMC' in str(newdata): 
#	if newdata == "b'$GNRMC":
		print("")
		print(newdata)
		print(newdata[20:29])
		print(newdata[32:42])
# 		N = str(newdata[20:29])
# 		N = re.sub("|\b|\'|\'", "", N)
# 		N = str(re.sub("b", "", N))
# 		N = int(float(N))
# 		print(N/100)
# 		
# 		W = str(newdata[32:42])
# 		W = re.sub("|\b|\'|\'", "", W)
# 		W = str(re.sub("b", "", W))
# 		W = int(float(W))
# 		print(W/100)
# 		newmsg=pynmea2.parse(newdata)
# 		lat=newmsg.latitude
# 		lng=newmsg.longitude
# 		gps = "Latitude=" + str(lat) + "and Longitude=" + str(lng)
# 		print(gps)