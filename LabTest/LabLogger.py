import time
from time import sleep, strftime
from datetime import datetime
import FunctionManager as FM

import os
import sys
import csv

import minimalmodbus
minimalmodbus.BAUDRATE = 9600
minimalmodbus.PARITY = 'N'
minimalmodbus.stopbits = 2

# Command to find serial ports
# python -m serial.tools.list_ports
flow_device_location = '/dev/cu.usbserial-14240'
flow_reader_address = 247

dynaLoad_location = '/dev/cu.usbmodem1411'
dynaLoad_address = 0

error = ""

if os.path.exists(flow_device_location):
	flow_reader = minimalmodbus.Instrument(flow_device_location, flow_reader_address)
	_isFlowReading = True
else:
	error = error + "\nEither FLOW METER is not connected properly or the device location needs to be updated in the code \n"
	error = error + "See README for instructions \n"
	_isFlowReading = False

if os.path.exists(dynaLoad_location):
    dynaLoad_reader = minimalmodbus.Instrument(dynaLoad_location, dynaLoad_address)
    _isDynaLoadReading = True
else:
    error = error + "\nEither DYNAMIC LOAD is not connected properly or the device location needs to be updated in the code \n"
    error = error + "See README for instructions \n"
    _isDynaLoadReading = False

# nominal_voltage = 80
# nominal_current = 45
# nominal_power = 600
# max_resolution = 52428

log_interval = 500 # milliseconds
t_delta = 0
runTime = 0

dateString = time.strftime("%Y-%m-%d")
folderDir = "TestData/LabData_" + dateString + '/'

if not os.path.exists(folderDir):
    os.system("sudo mkdir " + folderDir)

# def fileName(i):
#     return "labData_" + dateString + "_test" + str(i) + ".csv"

i = 1
while os.path.exists(folderDir + FM.FunctionManager.fileName(i)):
	i += 1

data = []
logFile = open(folderDir + FM.FunctionManager.fileName(i), 'a')

if os.stat(folderDir + FM.FunctionManager.fileName(i)).st_size == 0:
    logFile.write("Time,Time Delta (s),Gas Flow (l/min),Total Flow (l),Voltage (V),Set Current (A),Actual Current (A),Power (W)\n")

startTime = datetime.now()

with logFile:
    while True:

    # first arg:
    # 0: gas flow (l/min)
    # 4: total litres since start (l)
        # t1 = datetime.now().strftime("%S.%f")
        t1 = datetime.now()

        currentTime = datetime.now().strftime("%H:%M:%S.%f")
        if _isFlowReading:
            gasFlow = flow_reader.read_float(0,3)
            totalFlow = flow_reader.read_float(4,3)
        else:
            gasFlow = 0
            totalFlow = 0

        if _isDynaLoadReading:
            voltage_reading = dynaLoad_reader.read_register(507)
            # voltage = round(voltage_reading * nominal_voltage / float(max_resolution)), 3)
            voltage = round(FM.FunctionManager.readValToActualVal(voltage_reading, "Voltage"),3)

            current_reading = dynaLoad_reader.read_register(508)
            current = round(FM.FunctionManager.readValToActualVal(current_reading, "Current"),3)
            
            set_current_reading = dynaLoad_reader.read_register(502)
            set_current = round(FM.FunctionManager.readValToActualVal(set_current_reading, "Current"),3)

            power_reading = dynaLoad_reader.read_register(509)
            power = round(FM.FunctionManager.readValToActualVal(power_reading, "Power"), 2)
        else:
            voltage = 0
            current = 0
            power = 0
        
        runTime = int((datetime.now() - startTime).total_seconds())

        # Prints all of the data to the terminal
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Flow: " + str(gasFlow) + " l/min")
        print("Total Flow: " + str(totalFlow) + " l")
        print("Voltage: " + str(voltage) + " V")
        print("Set Current " + str(set_current) + " A")
        print("Current: " + str(current) + " A")
        print("Power: " + str(power) + " W")
        print("Time Delta: " + str(t_delta) + " ms")
        print("Runtime: " + str(runTime) + " s")
        if error is not "":
            print("***ERROR***: " + error)

        data = [currentTime,t_delta,gasFlow,totalFlow,voltage,set_current,current,power]
        writer = csv.writer(logFile)
        writer.writerow(data)

        t2 = datetime.now()
        t_delta = int((t2 - t1).total_seconds() * 1000) # milliseconds

        if (t_delta < log_interval):
        	sleep((log_interval - t_delta)/1000)
