import os
import sys
import csv
import time
from time import sleep, strftime
from datetime import datetime

timeString = time.strftime("%d-%m-%y")
folderDir = "FlowData_" + timeString + '/'
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

        date = datetime.now().strftime("%d/%m/%Y") + ","
        time = datetime.now().strftime("%H:%M:%S.%f") + ","
        # gasFlow = instr.read_float(0,3)
        # totalFlow = instr.read_float(4,3)

        # print(str(gasFlow) + ", ")
        # print(str(totalFlow) + "\n")

        data = [date,time]
        writer = csv.writer(myFile)
        writer.writerow(data)
        # print("Writing complete")
        t2 = datetime.now().strftime("%S.%f")
        t_delta = float(t2) - float(t1)
        print(t2)
        print(t_delta)