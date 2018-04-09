import time
from time import sleep, strftime
from datetime import datetime

class FunctionManager():

	@classmethod
	def fileName(self, i):
		dateString = time.strftime("%Y-%m-%d")
		return "labData_" + dateString + "_test" + str(i) + ".csv"

	@classmethod
	def readValToActualVal(self, reading, parameter):
		
		
		
		max_resolution = 52428

		if parameter == "Voltage":
			nominal_voltage = 80
			nominal_value = nominal_voltage
		elif parameter == "Current":
			nominal_current = 45
			nominal_value = nominal_current
		elif parameter == "Power":
			nominal_power = 600
			nominal_value = nominal_power

		return reading * nominal_value / float(max_resolution)