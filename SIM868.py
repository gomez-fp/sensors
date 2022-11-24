import serial
import time
from decimal import *
from subprocess import call
 
def find(str, ch):
    for i, ltr in enumerate(str):
        if ltr == ch:
            yield i
 
port = serial.Serial("/dev/ttyAMA0", baudrate=115200, timeout=1)
 
W_buff = 'AT'+'\r\n'
port.write(W_buff.encode())
rcv = port.read(100)
print (rcv)
time.sleep(.1) 
                                        # to power the GPS
W_buff = 'AT+CGNSPWR=1'+'\r\n'
port.write(W_buff.encode())
rcv = port.read(100)
print (rcv)
time.sleep(.1)
 
                                        # Set the baud rate of GPS
W_buff = 'AT+CGNSIPR=115200'+'\r\n'
port.write(W_buff.encode())
rcv = port.read(100)
print (rcv)
time.sleep(.1)
 
                                        # Send data received to UART
W_buff = 'AT+CGNSTST=1'+'\r\n'
port.write(W_buff.encode())
rcv = port.read(100)
print (rcv)
time.sleep(.1)
 
                                         # Print the GPS information
W_buff = 'AT+CGNSINF'+'\r\n'
port.write(W_buff.encode())
rcv = port.read(200)
#print (rcv)
time.sleep(.1)
ck=1
while ck==1:
    fd = port.read(200)        # Read the GPS data from UART
    #print(fd)
    fd = str(fd)
    time.sleep(.5)
    if '$GNRMC' in fd:        # To Extract Lattitude and 
        ps=fd.find('$GNRMC')        # Longitude
        dif=len(fd)-ps
        if dif > 50:
            data=fd[ps:(ps+50)]
            print (data)
            ds=data.find('A')        # Check GPS is valid
            if ds > 0 and ds < 20:
                p=list(find(data, ","))
                print("p es ", type(p))
                lat=data[(p[2]+1):p[3]]
                lon=data[(p[4]+1):p[5]]
                print("lat es ", lat)
 
# GPS data calculation
 
                s1=lat[2:len(lat)]
                s1=Decimal(s1)
                s1=s1/60
                s11=int(lat[0:2])
                s1 = s11+s1
 
                s2=lon[3:len(lon)]
                s2=Decimal(s2)
                s2=s2/60
                s22=int(lon[0:3])
                s2 = s22+s2
 
                print (s1)
                print (s2)