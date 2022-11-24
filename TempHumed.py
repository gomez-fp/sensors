import smbus
import time

while True:
	bus = smbus.SMBus(1)
	bus.write_i2c_block_data(0x44, 0x2C, [0x0D]) 
	time.sleep(0.5)
	 
	data = bus.read_i2c_block_data(0x44, 0x00, 6)
 
	# Convert the data
	temp = data[0] * 256 + data[1]
	#formulas deifinidas por el fabricante del sensor
	cTemp = round(-45 + (175 * temp / 65535.0), 2)
	cTemp1 = round(-48 + (175 * temp / 65535.0), 2)
#	humidity = round((100 * (data[3] * 256 + data[4]) / 65535.0),2)
	humidity = round((110 * (data[3] * 256 + data[4]) / 65535.0),2)
	 
	# Output data to screen
#	print('{0}, {1}, {2}°C, {3}%HR\r'.format(time.strftime('%m/%d/%y'), time.strftime('%H:%M:%S'), cTemp, humidity))
	print("Temperature: ", cTemp, "°C")
	print("Temperature2: ", cTemp1, "°C")#
	print("Humidity   : ", humidity,"%HR")
	time.sleep(0.5)