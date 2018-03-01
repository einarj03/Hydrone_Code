import minimalmodbus
import time
from time import sleep, strftime
from datetime import datetime
minimalmodbus.BAUDRATE = 9600
minimalmodbus.PARITY = 'N'
minimalmodbus.stopbits = 2

# Command to find serial ports
# python -m serial.tools.list_ports
device_location = '/dev/cu.usbmodem1411'

instr = minimalmodbus.Instrument(device_location, 0)
instr.address = 0

import os
import sys
import csv

nominal_voltage = 80
nominal_current = 45
nominal_power = 600
max_resolution = 52428

# instrument.get_all_pattern_variables(0)

timeString = time.strftime("%d-%m-%y")
folderDir = "FlowData/FlowData_" + timeString + '/'
fileName = "flow_log.csv"

gasFlow = 0
totalFlow = 0

if not os.path.exists(folderDir):
    os.system("sudo mkdir " + folderDir)

data = []
myFile = open(folderDir + fileName, 'a')

if os.stat(folderDir + fileName).st_size == 0:
    myFile.write("Date,Time,Gas Flow (l/min),Total Flow (l),Voltage (V),Current (A),Power (W)\n")

while True:
	os.system('cls' if os.name == 'nt' else 'clear')

	date = datetime.now().strftime("%d/%m/%Y")
	time = datetime.now().strftime("%H:%M:%S.%f")

	voltage_reading = instr.read_register(500)
	voltage = round((voltage_reading * nominal_voltage / max_resolution), 2)
	print("Voltage: " + str(voltage) + " V")

	current_reading = instr.read_register(501)
	current = round((current_reading * nominal_current / max_resolution), 2)
	print("Current: " + str(current) + " A")

	power_reading = instr.read_register(502)
	power = round((power_reading * nominal_power / max_resolution), 1)
	print("Power: " + str(power) + " W")

	data = [date,time,gasFlow,totalFlow,voltage,current,power]
	writer = csv.writer(myFile)
	writer.writerow(data)

	sleep(0.5)
