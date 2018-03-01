# to run this program, open terminal, cd into the right directory and type:
# python FlowReader.py

# to install minimalmodbus open terminal and type: 
# pip install minimalmodbus
import minimalmodbus
import time
from time import sleep, strftime
from datetime import datetime
minimalmodbus.BAUDRATE = 9600
minimalmodbus.PARITY = 'N'
minimalmodbus.stopbits = 2

# Command to find serial ports
# python -m serial.tools.list_ports
flow_device_location = '/dev/cu.usbserial-1420'
flow_reader_address = 247

dynaLoad_location = '/dev/cu.usbmodem1411'
dynaLoad_address = 0

flow_reader = minimalmodbus.Instrument(flow_device_location, flow_reader_address)
dynaLoad_reader = minimalmodbus.Instrument(dynaLoad_location, dynaLoad_address)
nominal_voltage = 80
nominal_current = 45
nominal_power = 600
max_resolution = 52428


import os
import sys
import csv

timeString = time.strftime("%d-%m-%y")
folderDir = "TestData/TestData_" + timeString + '/'
fileName = "test_data.csv"

if not os.path.exists(folderDir):
    os.system("sudo mkdir " + folderDir)

data = []
myFile = open(folderDir + fileName, 'a')

if os.stat(folderDir + fileName).st_size == 0:
    myFile.write("Date,Time,Gas Flow (l/min),Total Flow (l),Voltage (V),Current (A),Power (W)\n")

with myFile:
    while True:

    # first arg:
    # 0: gas flow (l/min)
    # 4: total litres since start (l)
        t1 = datetime.now().strftime("%S.%f")

        date = datetime.now().strftime("%d/%m/%Y")
        time = datetime.now().strftime("%H:%M:%S.%f")
        gasFlow = flow_reader.read_float(0,3)
        totalFlow = flow_reader.read_float(4,3)

        voltage_reading = instr.read_register(500)
        voltage = round((voltage_reading * nominal_voltage / max_resolution), 2)

        current_reading = instr.read_register(501)
        current = round((current_reading * nominal_current / max_resolution), 2)
        
        power_reading = instr.read_register(502)
        power = round((power_reading * nominal_power / max_resolution), 1)
        
        # Prints all of the data to the terminal
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Flow: " + str(gasFlow) + " l/min")
        print("Total Flow: " + str(totalFlow) + " l")
        print("Voltage: " + str(voltage) + " V")
        print("Current: " + str(current) + " A")
        print("Power: " + str(power) + " W")

        data = [date,time,gasFlow,totalFlow,voltage,current,power]
        writer = csv.writer(myFile)
        writer.writerow(data)
        # print("Writing complete")
        t2 = datetime.now().strftime("%S.%f")
        t_delta = float(t2) - float(t1)

        if (t_delta < 0.5 and t_delta > 0):
            sleep(.5-t_delta)
        elif t_delta < 0 and (60 + t_delta) < 0.5:
            sleep(0.5 - 60 - t_delta)