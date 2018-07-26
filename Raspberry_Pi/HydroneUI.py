import DataManager as DM

if DM.isRaspberryPi:
    from Tkinter import Tk
else:
    from tkinter import Tk

import Lib

#Setup the various cycle times


#Initilse and run UIs
root = Tk()
my_gui = Lib.DashGUI(root)
root.mainloop()