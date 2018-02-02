#https://cdn-learn.adafruit.com/downloads/pdf/adafruit-ultimate-gps-on-the-raspberry-pi.pdf
#http://www.danmandle.com/blog/getting-gpsd-to-work-with-python/

import numpy as np
from Tkinter import *
import tkFont
import DataManager as DM
import time
#import RPi.GPIO as GPIO
                
class DashGUI: 
    def __init__(self, master):
        #Setup variables that will be displayed
        #self.lastTime = time.time()
        
        self.Speed = StringVar()
        self.splitTimes = [StringVar(),StringVar(),StringVar(),StringVar(),StringVar()]
        self.CA=[]
        self.SC=[]

        #Fonts
        sectionTitle = tkFont.Font(family = 'Helvetica', size = 30, weight = 'bold')
        general = tkFont.Font(family = 'Helvetica', size = 30)
        
        """screen is 800x480 """
        self.master = master
        master.title("Alta")
        master.geometry("800x480")
        master.configure(background='black')
        
        #Create sections
        self.labelSect = Frame(master, bg='black')
        self.labelSect.grid(row=0, column=1, sticky=N+W)
        self.timesSect = Frame(master, bg='black')
        self.timesSect.grid(row=1, column=1, sticky=N+W)
        self.actSect = Frame(master, bg='black')
        self.actSect.grid(row=2, column=1, sticky=N+W)
        
        #Labels
        
        #Speed
#        Label(self.labelSect, text="Speed", bg='black',font=(None,52), fg='white').grid(row=0, sticky=N+W)
        self.labelSpeed = Label(self.labelSect, text="Speed", textvariable=self.Speed, font=(None,50), bg='black', fg='white')
        self.labelSpeed.grid(columnspan=2, sticky=N+W)
        

    
        #Control Output 
#        Label(self.labelSect, text="Control Action", font=(None,52), bg='black', fg='white').grid(row=1, column=0, sticky=N+W)
        self.labelCA = Label(self.labelSect, text="Control Action", textvariable=self.CA, font=(None,50), bg='black', fg='white')
        self.labelCA.grid(row=1, columnspan=2)
        
        #SuperCaps
#        Label(self.labelSect, text="SC %", font=sectionTitle, bg='black', fg='white').grid(row=2, sticky=N+W)
##        self.labelSCX = Label(self.labelSect, text="SC %",textvariable=self.SCX, font=(None,30), bg='black', fg='white')
##        self.labelSCX.grid(row=2, columnspan=2)
##    
        #Super Capacitor Status 
#        Label(self.labelSect, text="Super Caps", font=(None,12), bg='black', fg='white').grid(row=3, columnspan=3)
       
        self.labelSC1 = Label(self.labelSect, text="Danger", textvariable=self.SC,font=(None,20), bg='black', fg='white')
        self.labelSC1.grid(row=3, columnspan=2)
        self.labelSC2 = Label(self.labelSect, text="Moderate", textvariable=self.SC,font=(None,20),  bg='black', fg='white')
        self.labelSC2.grid(row=4, column=0,  columnspan=2)
        self.labelSC3 = Label(self.labelSect, text="Charged", textvariable=self.SC, font=(None,20), bg='black', fg='white')
        self.labelSC3.grid(row=5, columnspan=2)
        

#         self.labelSC3 = Label(self.labelSect, text="SC1", textvariable=self.SC, font=(None,5),height=3, width=3, bg='black', fg='white')
#        self.labelSC3.grid(row=6, columnspan=3, padx=0, pady=0)
        #Times
        Label(self.timesSect, text="Lap Times", font=(None,12), bg='black', fg='white').grid(row=0, columnspan=2)
        self.splitTimeLabels = range(3)
        for i in range(3):
            self.splitTimeLabels[i] = Label(self.timesSect, textvariable=self.splitTimes[i], font=(None,12), bg='black', fg='white')
            self.splitTimeLabels[i].grid(row=i+1, column=1)
#        for i in range(10):
#            self.splitTimeLabels[i] = Label(self.timesSect, textvariable=self.splitTimes[i], font=(None,12), bg='black', fg='white')
#            self.splitTimeLabels[i].grid(row=i+1, column=2)
#            
        
        #Actions
        self.start_button = Button(self.actSect, font=(None,12), text="Start", command=DM.DataManager.startIdealLap)
        self.start_button.grid(row=1, column=0)
        
        self.stop_button = Button(self.actSect, text="Stop",font=(None,12), command= DM.DataManager.stopLog)
        self.stop_button.grid(row=1, column=1)

        #self.close_button = Button(master, text="Exit", command= master.quit)
        #self.close_button.pack()
        
        #Speed slider
        self.speedSlide = Scale(master, from_=0, to=30, length=500, resolution=1, borderwidth=0, orient=HORIZONTAL, bg="grey")
        self.speedSlide.grid(row=3, columnspan=2, sticky=S)
        
        #map
        mapPlot = MiniMap(master)
        mapPlot.grid(row=0, column=0, rowspan=3)
        mapPlot.plotMap()
        
        mapPlot.startPosTracking()

        DM.DataManager.beginSerialReading()

        self.update() # starts the update loop
        
    def update(self):

        dataString = DM.DataManager.getArduinoDataString()

        speed = DM.DataManager.getArduinoData(dataString, 'Speed')
        if speed is not None:
            if speed % 1 == 0:
                self.Speed.set("%g" % speed + ".0" + " m/s")
            else:
                self.Speed.set("%g" % round(speed,1) + " m/s")
        else:
            self.Speed.set("-")
        
        SC = DM.DataManager.getArduinoData(dataString, 'Vsc') 
        self.speedSlide.set(SC)

        if SC < 15:
#           self.labelSC1["text"] = "Charging"
            self.labelSC1["background"] = "red"
            self.labelSC2["background"] = "black"
            self.labelSC3["background"] = "black"
  
        elif SC >= 15 and SC < 27:
#            self.labelSC1["text"] = "Discharging"
            self.labelSC1["background"] = "black"
            self.labelSC2["background"] = "orange"
            self.labelSC3["background"] = "black"
        
        else:
#           self.labelSC1["text"] = "Charging"
            self.labelSC1["background"] = "black"
            self.labelSC2["background"] = "black"
            self.labelSC3["background"] = "green"

        if DM.DataManager.ControlAction(speed):
            self.labelCA["text"] = "BOOST"
            self.labelCA["background"] = "blue"
        else:
            self.labelCA["text"] = "COAST"
            self.labelCA["background"] = "black"

        i = 0
        for Val in DM.DataManager.lineCrossTimes:
            if i > 0 and i < 6:
                split = DM.DataManager.lineCrossTimes[i-1] - Val
                self.splitTimes[i-1].set("%gs" % round(split,3))
            i += 1
            
        posI = DM.DataManager.getPosID()
        # posI1 = DM.DataManager.getPosID1()
        
#        simData = DM.DataManager.getSim()
#        if simData is not None:
#            self.speedSlide.set == SC
        
        self.master.update_idletasks()

        DM.DataManager.checkSwitch()

        DM.DataManager.logData(dataString)
        
        #print 1/(time.time()-self.lastTime)
        #self.lastTime = time.time()
        self.master.after(100, self.update)

        
class MiniMap(Canvas):
    def __init__(self,master,*args,**kwargs):
        #http://stackoverflow.com/questions/14389918/inherit-from-tkinter-canvas-calling-super-leads-to-error
        Canvas.__init__(self, master=master, *args, **kwargs)
        
        self.xScale = 1
        self.yScale = 1
        self.xTrans = 0
        self.yTrans = 0
       
        self.posPoint1 = False
        self.posPoint = False
        self.lastSide = None
        self.finLine = False
        
        self.size = 300
        self.margin = 20
        
        self.refreshTime = 100
        
        self.config(width=(self.size + 2*self.margin), height=(self.size + 2*self.margin), background='black', highlightbackground='black')
        
        
    def plotMap(self):
        """Process track (and calabrate)"""
        data = DM.DataManager.getTrackData('LongLat')
        
        #Move the map so all positive from 0
        minInDir = data.min(axis=0)
        
        self.xTrans = minInDir[0] * -1
        self.yTrans = minInDir[1] * -1
        data[:,0] += self.xTrans
        data[:,1] += self.yTrans
        
        
        #Scale the map for screen co-ordinates
        maxInDir = data.max(axis=0)
        scaleInDir = self.size/maxInDir
        
        self.xScale = scaleInDir[0]
        self.yScale = scaleInDir[1]
        data[:,0] *= scaleInDir[0]
        data[:,1] *= scaleInDir[1]
        
        #Flip so map points north
        data[:,1]  = (data[:,1]*-1)+self.size
        
        #Add margins
        data += self.margin
        
        i = 0
        for row in data:
            if i == 0:
                self.create_line((row[0], row[1], data[-1][0], data[-1][1]), fill="white", width=2)
            else:
                self.create_line((row[0], row[1], data[i-1][0], data[i-1][1]), fill="white", width=2)
                
            i = i+1
            
            
        """Process finish line"""
        finData = self.posToPixel(np.genfromtxt('FinishCoOrds_Final.csv', delimiter=','))
        self.finLine = finData
        self.create_line((finData[0,0], finData[0,1], finData[1,0], finData[1,1]), fill="red")
        
    def startPosTracking(self):
        if DM.DataManager.idealLap:
            gpsLL1 = DM.DataManager.getIdealGPSPos()
            if gpsLL1 is not None:    
                LongLat = self.posToPixel(gpsLL1)
                Long = LongLat[0,0]
                Lat = LongLat[0,1]
                
                if self.posPoint1 is False:
                    self.posPoint1 = self.create_rectangle((Long-10, Lat-10, Long+10, Lat+10), fill="yellow")

                else:
                    self.coords(self.posPoint1, (Long-10, Lat-10, Long+10, Lat+10))

        gpsLL = DM.DataManager.getGPSPos()
        if gpsLL is not None:

            gpsPos = DM.DataManager.getPosID()
            trackLLData = DM.DataManager.getTrackData("LongLat")

            trackLL = [trackLLData[gpsPos,0],trackLLData[gpsPos,1]]

            LongLat = self.posToPixel(trackLL)
            Long = LongLat[0,0]
            Lat = LongLat[0,1]
            
            if self.posPoint is False:
                self.posPoint = self.create_oval((Long-10, Lat-10, Long+10, Lat+10), fill="red")

            else:
                self.coords(self.posPoint, (Long-10, Lat-10, Long+10, Lat+10))

            #http://stackoverflow.com/questions/22668659/calculate-on-which-side-of-a-line-a-point-is
            x0, y0 = self.finLine[0,0], self.finLine[0,1]
            x1, y1 = self.finLine[1,0], self.finLine[1,1]
            x2, y2 = Long, Lat

            value = ((x1 - x0)*(y2 - y0)) - ((x2 - x0)*(y1 - y0))

            #True is greater than 0, right hand side
            #So false to true for going clockwise
            if self.lastSide is None:
                self.lastSide = (value > 0)
            else:
                if self.lastSide == True and (value > 0):
                    DM.DataManager.lineCrossTimes.insert(0, time.time())

                self.lastSide = (value < 0)
        
        self.master.after(self.refreshTime, self.startPosTracking)
        
#    Convert long and lat data into pixels
    def posToPixel(self, data):
        if isinstance(data, list):
            data = np.asarray([data])
        
        data[:,0] = (data[:,0] + self.xTrans) * self.xScale
        data[:,1] = (data[:,1] + self.yTrans) * self.yScale
        data[:,1]  = (data[:,1]*-1) + self.size
        data += self.margin
        
        return data
