#https://cdn-learn.adafruit.com/downloads/pdf/adafruit-ultimate-gps-on-the-raspberry-pi.pdf
#http://www.danmandle.com/blog/getting-gpsd-to-work-with-python/

# -*- coding: utf-8 -*-

import random
from random import randint, choice
import time
from time import sleep, strftime
import datetime
import os
import csv
import numpy as np
import Threads as Thrd
import serial
import math
import minimalmodbus

from datetime import datetime

# instr.read_float(0,3)
# first arg:
    # 0: gas flow (l/min)
    # 4: total litres since start (l)

# This variable is for debugging purposes on the computer
isRaspberryPi = False

if isRaspberryPi:
    # initialising GPIO pins
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(10, GPIO.IN) # pin 19
    GPIO.setup(12, GPIO.IN) # pin 32
    GPIO.setup(13, GPIO.IN) # pin 33
    GPIO.setup(14, GPIO.IN) # pin 8
    GPIO.setup(19, GPIO.IN) # pin 35
    GPIO.setwarnings(False)

class DataManager():
    isEmulate = False
    idealLap = False
    isRecording = False
    startTime = 0
    _dataFile = False
    _trackFile = False
    _idealLapFile = False
    _gpsSession = False
    _hallSpeedSess = False
    _simSession = False
    test = False
    isCurrentlyBoosting = False
    rwThread = False
    isCarVersion = True
    # reportTest = True
    emulate_gps = True
    _isFlowLoggin = False

    # If the program is running on the raspberry pi then set the flow meter and 
    # serial variables
    if isRaspberryPi:
        if _isFlowLoggin:
            # conifguring the fuel flow rate measuring parameters
            minimalmodbus.BAUDRATE = 9600
            minimalmodbus.PARITY = 'N'
            minimalmodbus.stopbits = 2
            # device_location is different for RPi
            # Command to find serial ports
            # python -m serial.tools.list_ports
            device_location = '/dev/ttyUSB0'

            instr = minimalmodbus.Instrument(device_location, 1)
            instr.address = 247

        ser = serial.Serial('/dev/ttyACM0', 9600, 8, 'N', 1, timeout=5)

        folderDir = "/home/pi/Desktop/RunData/RunData_"+time.strftime("%d-%m-%y")+'/'
        fileName = "data_log.csv"

    # only start the gps session if we are not emulating the gps
    if not (isEmulate or emulate_gps): 
        global gpsSession
        gpsSession = gpsdExporter.GpsPoller()
        gpsSession.start()
    
    # Calcaulted variabels
    lineCrossTimes = []

    # For debugging on the computer, set the number of different variables normally 
    # recieved from the arduino
    numOfArduinoData = 4

    emuPosI = 0
    emuPosI1 = 0

    # retrieves the LongLat coords of the track
    @classmethod
    def getTrackData(self, colName = False):
        if DataManager._trackFile is False:
            DataManager._trackFile = np.loadtxt('trackPoints.csv', delimiter=',')
            
        #1 - 'Index' -  Index, for usefullness
        #2,3 - 'LongLat' - GPS Long and Lat
        #4 - 'Alt' - GPS Altitude
        
        if colName is False:
            return DataManager._trackFile
        elif colName == "Index":
            return DataManager._trackFile[:,0]
        elif colName == "LongLat":
            return DataManager._trackFile[:,[1,2]]
    

    # uses the current position along the track and the current speed to 
    # determine the necessary Control Action
    @classmethod
    def ControlAction(self, speed):
        gpsID = DataManager.getPosID()
        # speed = DataManager.getGPSSpeed()

        # first corner pulse
        if gpsID >= 100 and gpsID <= 151:
            if DataManager.isCurrentlyBoosting:
                if speed > 7.7:
                    DataManager.isCurrentlyBoosting = False
                    return False
                else:
                    return True

            else: 
                if speed < 5.4:
                    DataManager.isCurrentlyBoosting = True
                    return True
                else:
                    return False

        # hill pulse
        elif gpsID >= 1273 and gpsID <= 1450:
            if DataManager.isCurrentlyBoosting:
                return True

            else: 
                if speed < 4.6:
                    DataManager.isCurrentlyBoosting = True
                    return True
                else:
                    return False
        else:
            DataManager.isCurrentlyBoosting = False
            return False

   
    # retrieves the ideal lap data 
    @classmethod
    def getIdealLapData(self, colName = False):
        if DataManager._idealLapFile is False:
            DataManager._idealLapFile = np.loadtxt('idealLapData.csv', delimiter=',')

        #1 - 'Index' -  Index, for usefullness
        #2,3 - 'LongLat' - GPS Long and Lat
        #4 - 'Alt' - GPS Altitude
        #7 - 'Time' - The car should be at the above coordinates by 
        #             this time after the race starts
        #8 - 'Speed' - Required speed at that point along the track

        if colName is False:
            return DataManager._idealLapFile
        elif colName == "Index":
            return DataManager._idealLapFile[:,0]
        elif colName == "LongLat":
            return DataManager._idealLapFile[:,[1,2]]
        elif colName == "Time":
            return DataManager._idealLapFile[:,3]
        elif colName == "Speed":
            return DataManager._idealLapFile[:,4]

    @classmethod
    def readGasFlow(self):
        # Only attempt to read the flow meter data if this is the RPi and flow logging
        # is requested
        if DataManager._isFlowLoggin and isRaspberryPi:
            gasFlow = instr.read_float(0,3)
        else:
            gasFlow = 0
        return gasFlow


    @classmethod
    def readTotalFlow(self):
        # Only attempt to read the flow meter data if this is the RPi and flow logging
        # is requested
        if DataManager._isFlowLoggin and isRaspberryPi:
            totalFlow = instr.read_float(4,3)
        else:
            totalFlow = 0
        return totalFlow

    @classmethod
    def getArduinoDataString(self):
        # Only attempt to read the arduino data if this is the RPi
        if isRaspberryPi:
            dataString = DataManager.ser.readline()
            while dataString.count(',', 1) != numOfArduinoData - 1:
                    # carry on reading a line from serial until all the data came through correctly
                    dataString = DataManager.ser.readline()
        # Otherwise, make a simulated dataString
        else:
            dataString = ""
            for i in range(1, DataManager.numOfArduinoData + 1):
                if i < DataManager.numOfArduinoData:
                    dataString = dataString + str(i) + ","
                else:
                    dataString = dataString + str(i)

        return dataString

    @classmethod
    def beginSerialReading(self):
        # Only attempt to read the arduino data if this is the RPi
        if isRaspberryPi:
            serialTest = DataManager.ser.readline()
            # if there are at least 3 commas starting from the second char within the string
            # then all 4 peices of data have come through
            for i in range(1,30):
                while serialTest.count(',', 1) != 3:
                    # carry on reading a line from serial until all the data came through correctly
                    serialTest = DataManager.ser.readline()
                i += 1


    @classmethod
    def getArduinoData(self, dataString, desiredData):
        time_diff, A0, A1, n_pings = dataString.split(',')
        time_diff = float(time_diff)
        n_pings = float(n_pings)
        A0 = float(A0)
        A1 = float(A1)
            
        secondsPerMin = 60
        millisPerS = 1000
        pingsPerRev = 6
        wheelRadius = 0.239

        if desiredData == 'RPM':
            RPM = secondsPerMin*millisPerS/(time_diff)*(n_pings/pingsPerRev)
            return round(RPM, 1)
        elif desiredData == 'Speed':

            # store and array of the last 6 points for each point, then you can take an average for each point
            # So send every point and then 
            speed = 2.0*math.pi*wheelRadius*millisPerS/(time_diff)*(n_pings/pingsPerRev)
            # m/s
            return round(speed, 1)


        elif desiredData == 'Vsc':
            # Super capacitor voltage

            # A0 outputs values between 0-1023 for a voltage range of 0-5V
            # The resistor setup reduces the read voltage by a factor of 26
            Vsc = A0 * 5 * 26 / 1023
            return round(Vsc, 1)

        elif desiredData == 'Vmain':
            # Mainline voltage
            Vmain = A1 * 5 * 26 / 1023
            return round(Vmain, 1)


    # gets the speed using Hall sensors
    # (currently not in use)
    @classmethod
    def getSpeed(self):
        if DataManager._hallSpeedSess is False:
            DataManager._hallSpeedSess = Thrd.HallSensors(DataManager.isEmulate)
            DataManager._hallSpeedSess.start()
        
        TotS = 0;
        for i in range(1,3):
            obj = DataManager._hallSpeedSess;
            TotS = TotS + (obj.stamps[i][0] - obj.stamps[i][1])
            
        return 1/((TotS/6)*21) #rev/s%%
    
    # old method of getting the gps data
    # (currently not in use)
    @classmethod
    def getGPSReport(self):
        if DataManager._gpsSession is False:
            #This starts a thread which self connects
            DataManager._gpsSession = Thrd.GpsPoller()
            DataManager._gpsSession.start()
        
        return DataManager._gpsSession.curReport
    
    @classmethod
    def getSim(self):
        if DataManager._simSession is False:
            DataManager._simSession = Thrd.SimThread()
            DataManager._simSession.start()
        
        return DataManager._simSession.simStore
    
    # initialises the variables required to display the ideal lap icon
    @classmethod
    def startIdealLap(self):
        DataManager.startTime = time.time()
        DataManager.idealLap = True        

    # uses the time difference between the current time and when the ideal lap 
    # button was pressed to figure out which point from the ideal lap strategy to use
    @classmethod
    def getIdealPosID(self):
        
        timeDiff = DataManager.getTimeDiff()
        trackTimes = DataManager.getIdealLapData('Time')
        
        Dif = np.absolute(np.subtract(timeDiff, trackTimes))
        return np.argmin(Dif)

    # uses the ID of the current ideal lap position to find the corresponding
    # ideal lap coordinates
    @classmethod
    def getIdealGPSPos(self):
        idealLapID = DataManager.getIdealPosID()

        idealLapLL = DataManager.getIdealLapData('LongLat')

        return [idealLapLL[idealLapID, 0], idealLapLL[idealLapID, 1]]

    # gets the difference between the current time and when the ideal lap 
    # button was pressed
    @classmethod
    def getTimeDiff(self):
        timeNow = time.time()
        return timeNow - DataManager.startTime

    # returns the current LongLat coordinates of the gps
    @classmethod
    def getGPSPos(self):
        if DataManager.isEmulate or DataManager.emulate_gps:
            # emulates the location by moving the icon forward 4 points every iteration
            LL = DataManager.getTrackData('LongLat')
 
            self.emuPosI += 4
            if self.emuPosI >= len(LL):
                self.emuPosI = 0

            return [LL[self.emuPosI,0], LL[self.emuPosI,1]]

        else:
            # print "GPS Coords: ", str([gpsSession.longitude, gpsSession.latitude])
            return [gpsSession.longitude, gpsSession.latitude]
                
        return None
    
    # uses the current gps coordinates to find the closest corresponding point
    # in the track data file. This is to be able to display the driver's icon
    # on the map
    @classmethod
    def getPosID(self):
        LongLat = DataManager.getGPSPos()
        TrackLongLat = DataManager.getTrackData('LongLat')
        
        Dif = np.absolute(np.subtract(LongLat, TrackLongLat))
        Tot = np.sum(Dif, axis=1)
        return np.argmin(Tot)
    
    # gets the current gps speed
    @classmethod
    def getGPSSpeed(self):
        if DataManager.isEmulate:
            # randomise a speed from 1-10
            return random.uniform(1,10)
        else:
            return gpsSession.speed
        
        return None
    
    # use the GPIO inputs to determine the SuperCapacitor status
    @classmethod
    def getSCstatus(self):
        if DataManager.isEmulate:
            return 7
        else:
            if GPIO.input(12)==0 and GPIO.input(13)==0 and GPIO.input(14)==0 and GPIO.input(19)==1:
                            # print "X < 12 V"
                            return 1
            if GPIO.input(12)==1 and GPIO.input(13)==1 and GPIO.input(14)==0 and GPIO.input(19)==0:
                            # print "12<= X <=15"
                            return 2
            if GPIO.input(12)==1 and GPIO.input(13)==0 and GPIO.input(14)==1 and GPIO.input(19)==0:
                            # print "15< X <=18"
                            return 3
            if GPIO.input(12)==0 and GPIO.input(13)==1 and GPIO.input(14)==1 and GPIO.input(19)==0:
                            # print "18< X <=21"
                            return 4
            if GPIO.input(12)==0 and GPIO.input(13)==0 and GPIO.input(14)==1 and GPIO.input(19)==0:
                            # print "21< X <=24"
                            return 5
            if GPIO.input(12)==0 and GPIO.input(13)==1 and GPIO.input(14)==0 and GPIO.input(19)==0:
                            # print "24< X <=27"
                            return 6
            if GPIO.input(12)==1 and GPIO.input(13)==0 and GPIO.input(14)==0 and GPIO.input(19)==0:
                            # print "27< X <=30"
                            return 7
            if GPIO.input(12)==1 and GPIO.input(13)==1 and GPIO.input(14)==1 and GPIO.input(19)==0:
                            # print "X >=30"
                            return 8
            else:
                pass
    
    # (currently not in use) 
    @classmethod
    def getDataFile(self):
        if DataManager._dataFile is False:
            print("File opened")

            path = os.path.dirname(self.folderDir)
            if not os.path.exists(path):
                os.makedirs(path)
                
            DataManager._dataFile = open(DataManager.folderDir+time.strftime("%H:%M:%S")+'.log', "w")
            
        return DataManager._dataFile
    
    # checks to see if the ideal lap strategy button has been pressed
    @classmethod
    def checkSwitch(self):
        # only checks for the switch in the car version
        if DataManager.isCarVersion and isRaspberryPi:
            if (GPIO.input(10) == False):
                # if the button has been pressed then begin displaying the ideal lap
                # icon on the map
                DataManager.startIdealLap()

# logs one set of the data
    @classmethod
    def logData(self, dataString):
        # only log data if this is being run in the car (avoids two sets of data being recorded)
        if DataManager.isCarVersion and DataManager.isRecording and isRaspberryPi:
            # if the folders do not already exist, create them
            if not os.path.exists(DataManager.folderDir):
                os.mkdir(DataManager.folderDir)

            # open or create the log file
            file = open(DataManager.folderDir + DataManager.fileName, "a")

            # if the file is empty, then add the headings
            if os.stat(DataManager.folderDir + DataManager.fileName).st_size == 0:
                file.write("Date,Time,RPM,Speed,Vsc,Vmain,Gas Flow,Total Flow,Longitude,Latitude,Altitude,Climb\n")

            RPM = DataManager.getArduinoData(dataString, 'RPM')
            speed = DataManager.getArduinoData(dataString, 'Speed')
            Vsc = DataManager.getArduinoData(dataString, 'Vsc')
            Vmain = DataManager.getArduinoData(dataString, 'Vmain')
            gasFlow = DataManager.readGasFlow()
            totalFlow = DataManager.readTotalFlow()

            # record each pertinent piece of data
            file.write(str(time.strftime("%d/%m/%Y")) + ",")
            file.write(str(datetime.datetime.now().strftime("%H:%M:%S.%f")) + ",")
            file.write(str(RPM) + ",")
            file.write(str(speed) + ",")
            file.write(str(Vsc) + ",")
            file.write(str(Vmain) + ",")
            file.write(str(gasFlow) + ",")
            file.write(str(totalFlow) + ",")


            if not (DataManager.isEmulate or DataManager.emulate_gps):
                file.write(str(gpsSession.longitude) + ",")
                file.write(str(gpsSession.latitude) + ",")
                file.write(str(gpsSession.altitude) + ",")
                file.write(str(gpsSession.climb) + ",")

            file.write(str("\n"))

            # flush and close the file after every recording to ensure that all
            # data is saved even when the Pi is turned off suddenly
            file.flush()
            file.close()

    @classmethod
    def startLog(self):  
        #Make sure previous one is stopped
        # DataManager.test = True
        # DataManager.stopLog()
        
        DataManager.isRecording = True

        # DataManager.rwThread = Thrd.RWThread()
        # DataManager.isRecording = True
        # DataManager.rwThread.start()
       
    # stops the ideal lap icon from showing 
    @classmethod
    def stopLog(self):

        DataManager.isRecording = False
        # DataManager.idealLap = False

##        DataManager.isRecording = False
##        if DataManager.rwThread is not False:
##            DataManager.rwThread.cancel()
##
##        if DataManager._dataFile is not False:
##            DataManager._dataFile.close()
##            DataManager._dataFile = False
##            print("File closed")
            
    @classmethod
    def swapLog(self):
        if DataManager._dataFile is not False:
            DataManager._dataFile.close()
            DataManager._dataFile = False
            print("File swapped")
    
    def __del__(self):
        DataManager.rwThread.cancel()
        DataManager._gpsSession.cancel()
        DataManager._hallSpeedSess.cancel()
        
        if DataManager._dataFile is not False:
            print("File closed")
            DataManager._dataFile.close()
