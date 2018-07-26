import time
import serial
import pynmea2

gps_device_location = '/dev/ttyACM0'

ser = serial.Serial(gps_device_location, 9600, stopbits=2)  # open serial port

# streamreader = pynmea2.NMEAStreamReader()
# error = ""
# Read the first line of serial input without using 
data = ser.readline().decode().strip()
while True:
	data = ser.readline().decode().strip()
	print(data)
	# try:
	# 	msg = pynmea2.parse(data)
	# 	try:
	# 		print("Latitude: " + str(msg.latitude))
	# 		print("Longitude: " + str(msg.longitude))
	# 		# print(error)
	# 		break

	# 	except AttributeError:
	# 		# error = "AttributeError"
	# 		continue
	# except:
	# 	# error = "ParseError"
	# 	continue

    # print(msg.longitude)
    # print("MSG: " + str(msg) + "/n")
    # print("Lat: " + str(msg.lat) + "/n")


    # for msg in streamreader.next(data):
    #     print(msg)

	time.sleep(0.5)