The symbol below indicates that the text after it should be pasted into the Terminal and then executed by pressing the 'Enter' key
>> 

********
### INSTALLING THE RELEVANT TOOLS (Only needs to be done once per computer) ###
********

Install xCode from the App Store

Open Terminal

Type and press enter:
>> gcc

When the pop-up appears click install

Install Homebrew
>> /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"

Install Python
>> brew install python

Install Pip
>> sudo easy_install pip

Install minimalmodbus
>> pip install minimalmodbus



********
### RUNNING THE LAB LOGGER CODE ####
********

This code can record from both the flow meter and the dynamic load at this same time

1. Open Terminal

2. Find the location of the flowmeter and dynamic load
>> python -m serial.tools.list_ports

The flow meter location should look similar to the following:
/dev/cu.usbserial-14240

The dynamic load location should look similar to the following:
/dev/cu.usbmodem1411

3. Open the LabLogger.py file. Copy and paste the locations you found in Terminal into the flow_device_location and the dynaLoad_location variables respectively. Be sure not to accidentally delete the quotation marks.

4. Save the file.

5. Go back into Terminal. Change directory into the folder with the file:
>> cd Desktop/Hydrone_Code-master/LabTest/

6. Run the code:
>> sudo python LabLogger.py

7. Type in your computer password if prompted to do so