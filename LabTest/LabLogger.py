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

connection_error = ""

if os.path.exists(flow_device_location):
	flow_reader = minimalmodbus.Instrument(flow_device_location, flow_reader_address)
	_isFlowReading = True
else:
	connection_error += "\nEither FLOW METER is not connected properly or the device location needs to be updated in the code \n"
	connection_error += "See README for instructions \n"
	_isFlowReading = False

if os.path.exists(dynaLoad_location):
    dynaLoad_reader = minimalmodbus.Instrument(dynaLoad_location, dynaLoad_address)
    _isDynaLoadReading = True
else:
    connection_error += "\nEither DYNAMIC LOAD is not connected properly or the device location needs to be updated in the code \n"
    connection_error += "See README for instructions \n"
    _isDynaLoadReading = False

log_interval = 500 # milliseconds
t_delta = 0
run_time = 0

date_string = time.strftime("%Y-%m-%d")
folder_dir = "TestData/LabData_" + date_string + '/'

if not os.path.exists(folder_dir):
    os.system("sudo mkdir " + folder_dir)

i = 1
while os.path.exists(folder_dir + FM.FunctionManager.fileName(i)):
	i += 1

data = []
log_file = open(folder_dir + FM.FunctionManager.fileName(i), 'a')

if os.stat(folder_dir + FM.FunctionManager.fileName(i)).st_size == 0:
    log_file.write("Time,Time Delta (s),Runtime (s),Gas Flow (l/min),Total Flow (l),Voltage (V),Set Current (A),Actual Current (A),Power (W)\n")

start_time = datetime.now()

with log_file:
    while True:

    # first arg:
    # 0: gas flow (l/min)
    # 4: total litres since start (l)
        # t1 = datetime.now().strftime("%S.%f")
        t1 = datetime.now()

        current_time = datetime.now().strftime("%H:%M:%S.%f")
        if _isFlowReading:
            try:
                gas_flow = flow_reader.read_float(0,3)
                total_flow = flow_reader.read_float(4,3)
            except ValueError:
                flow_error = "\nFlow Meter READING error at "
                flow_error = t1.strftime("%H:%M:%S.%f") + "\n"
        else:
            gas_flow = 0
            total_flow = 0

        if _isDynaLoadReading:
            try:
                voltage_reading = dynaLoad_reader.read_register(507)
                # voltage = round(voltage_reading * nominal_voltage / float(max_resolution)), 3)
                voltage = round(FM.FunctionManager.readValToActualVal(voltage_reading, "Voltage"),2)

                current_reading = dynaLoad_reader.read_register(508)
                current = round(FM.FunctionManager.readValToActualVal(current_reading, "Current"),2)
                
                set_current_reading = dynaLoad_reader.read_register(501)
                set_current = round(FM.FunctionManager.readValToActualVal(set_current_reading, "Current"),2)

                power_reading = dynaLoad_reader.read_register(509)
                power = round(FM.FunctionManager.readValToActualVal(power_reading, "Power"), 1)
            except ValueError:
                dynaLoad_error = "\nDynamic Load READING error at "
                dynaLoad_error = t1.strftime("%H:%M:%S.%f") + "\n"
        else:
            voltage = 0
            current = 0
            set_current = 0
            power = 0
        
        printed_error = connection_error + flow_error + dynaLoad_error
        run_time = int((datetime.now() - start_time).total_seconds())
        m, s = divmod(run_time, 60)

        # Prints all of the data to the terminal
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Flow: " + str(round(gas_flow, 3)) + " l/min")
        print("Total Flow: " + str(round(total_flow,3)) + " l")
        print("Voltage: " + str(voltage) + " V")
        print("Set Current " + str(set_current) + " A")
        print("Current: " + str(current) + " A")
        print("Power: " + str(power) + " W")
        print("Time Delta: " + str(t_delta) + " ms")
        print("Runtime: " + str(m) + "mins " + str(s) + "secs")
        if printed_error is not "":
            print("***ERROR***: " + printed_error)

        data = [current_time,t_delta,run_time,gas_flow,total_flow,voltage,set_current,current,power]
        writer = csv.writer(log_file)
        writer.writerow(data)

        t2 = datetime.now()
        t_delta = int((t2 - t1).total_seconds() * 1000) # milliseconds

        if (t_delta < log_interval):
        	sleep((log_interval - t_delta)/1000)
