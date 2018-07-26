********
### INSTALLING THE RELEVANT TOOLS (Only needs to be done once per computer) ###
********

Install Pip
>> sudo easy_install pip

Install minimalmodbus
>> pip install minimalmodbus

Install pynmea2
>> pip install pynmea2

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
>> cd Desktop/Raspberry_Pi/

6. Run the code:
>> python HydroneUI.py