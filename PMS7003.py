from pms7003 import Pms7003Sensor, PmsSensorException
import RPi.GPIO as GPIO

if __name__ == '__main__':

    sensor = Pms7003Sensor('/dev/ttyUSB1')
    

    while True:
        try:
        
            #print(sensor.read())
            #print("")
            dic = sensor.read()
            #print("PM 1.0 =", dic['pm1_0cf1'], "PM 2.5 =", dic['pm2_5cf1'], "PM 10 =", dic['pm10cf1'])
            p1 = dic['pm1_0cf1']
            p2 = dic['pm2_5cf1']
            p10 = dic['pm10cf1']
            p1 = p1 
            p2 = p2
            p10 = p10 
            
            print("p1 = ", p1, "p2 = ", p2, "p10 = ", p10 )
            print("")
            
        except PmsSensorException:
            print('Connection problem')
            

    sensor.close()

