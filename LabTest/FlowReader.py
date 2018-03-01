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
device_location = '/dev/cu.usbserial-1420'

instr = minimalmodbus.Instrument(device_location, 1)
instr.address = 247

import os
import sys
import csv

timeString = time.strftime("%d-%m-%y")
folderDir = "FlowData/FlowData_" + timeString + '/'
fileName = "flow_log.csv"

if not os.path.exists(folderDir):
    os.system("sudo mkdir " + folderDir)

data = []
myFile = open(folderDir + fileName, 'a')

with myFile:
    while True:

    # first arg:
    # 0: gas flow (l/min)
    # 4: total litres since start (l)
        t1 = datetime.now().strftime("%S.%f")

        date = datetime.now().strftime("%d/%m/%Y")
        time = datetime.now().strftime("%H:%M:%S.%f")
        gasFlow = instr.read_float(0,3)
        totalFlow = instr.read_float(4,3)

        print(str(gasFlow) + ", ")
        print(str(totalFlow) + "\n")

        data = [date,time,gasFlow,totalFlow]
        writer = csv.writer(myFile)
        writer.writerow(data)
        # print("Writing complete")
        t2 = datetime.now().strftime("%S.%f")
        t_delta = float(t2) - float(t1)

        if (t_delta < 0.5 and t_delta > 0):
            sleep(.5-t_delta)
        elif t_delta < 0 and (60 + t_delta) < 0.5:
            sleep(0.5 - 60 - t_delta)


# file = open(folderDir + fileName, "a")

# file = open(folderDir + fileName, "a")

# with open(folderDir + fileName) as File:
    




# while False:
#     # first arg:
#     # 0: gas flow (l/min)
#     # 4: total litres since start (l)
#     # gasFlow = instr.read_float(0,3)
#     # print(gasFlow)
#     # totalFlow = instr.read_float(4,3)
#     # print time.strftime("%d/%m/%Y")
#     # file.write(str(time.strftime("%d/%m/%Y")) + ",")
#     # file.write(str(datetime.datetime.now().strftime("%H:%M:%S.%f")) + ",")

#     # file.write(str(gasFlow) + ",")
#     # file.write(str(totalFlow) + ",")

#     # file.write(str("\n"))

#     # flush and close the file after every recording to ensure that all
#     # data is saved even when the Pi is turned off suddenly
#     # file.flush()
#     # file.close()

#     sleep(.5)