import numpy as n
# conda install -c quasiben pyserial=2.7
import serial
import io
import time

# To instantiate a Uti class object call:
#> myUti = UtiClass.Uti(<port>)
# where <port> is an integer corresponding to the serial port to which the UTI is connected.
# This automatically connects to the port.
# Once a Uti object is created, the UTI board must be initialized, call:
#>> myUti.InitializeUti()
# which initializes the UTI to mode '2' by default (5 capacitors, 0-12 pF). If another mode is requested before this call:
#>> myUti.set_UTI_MODE(mode)
# where <mode> is a string corresponding to operation modes of the UTI:
#	'0' -> 5 capacitors, 0-2 pF
#	'1' -> 3 capacitors, 0-2 pF
#	'2' -> 5 capacitors, 0-12 pF
# To have the UTI board make a measurement call:
#>> raw_vals = myUti.PollUtiVals()
# To convert this to a capacitance call:
#>> cap_vals = myUti.CalculateCapacitance(raw_vals)
# this uses the default value of REF_CAP = 1.18, to change this call:
#>> myUti.set_REF_CAP(<val>)
# where <val> is the value of the reference capacitor in pF
# To save raw output to csv file call:
#>> myUti.LogRawValuesCsv(raw_vals)
# To save capacitance values to csv file call:
#>> myUti.LogCapValuesCsv(cap_vals)
# To close the serial connection to the UTI board call:
#>> myUti.SerialDisconnect()


class Uti:
	# Mode to run UTI in
	UTI_MODE = '2'
	# Number of capacitor level sensors attached to box
	N_SENSORS = 3
	# Number of capacitance readings output by UTI
	N_MEAS = N_SENSORS + 2
	def set_UTI_MODE(self, mode):
		if mode == '0':
			self.UTI_MODE = mode
			self.N_SENSORS = 5
		elif mode == '1':
			self.UTI_MODE = mode
			self.N_SENSORS = 3
		elif mode == '2':
			self.UTI_MODE = mode
			self.N_SENSORS = 5
		else:
			self.UTI_MODE = '2'
			self.N_SENSORS = 5
		self.N_MEAS = num+2
	def get_UTI_MODE(self):
		return UTI_MODE
	def get_N_MEAS(self):
		return self.N_SENSORS
	def get_N_MEAS(self):
		return self.N_SENSORS

	# Reference capacitor installed on UTI board (picofarads)
	REF_CAP = 1.28
	def set_REF_CAP(self, val):
		self.REF_CAP = val
	def get_REF_CAP(self):
		return self.REF_CAP
		
	# Path to data storage location
	DATA_PATH = 'C:\\Users\\Dylan\\Google Drive\\Research\\XENA-FOXe\\Level Sensors\\data\\'
	def set_DATA_PATH(self, path):
		self.DATA_PATH = path
	def get_DATA_PATH(self):
		return self.DATA_PATH

	# Connect to a port with specific properties
	# Arguments:
	#	port - string of the serial port to connect to, e.g. 'COM3'
	# Returns:
	# 	ser_obj - serial port object that is connected to port
	def SerialConnect(self, port):
		try:
			ser_obj = serial.Serial()
			ser_obj.baudrate = 19200
			ser_obj.port = port
			
			ser_obj.timeout=2
			ser_obj.bytesize=8
			ser_obj.parity='N'
			ser_obj.stopbits=1
			# if ser_obj.is_open: return ser_obj
			# else: return 0
			ser_obj.open()
			return ser_obj
		except serial.serialutil.SerialException:
			print 'Cannot connect to UTI - verify port'
			quit()
		
	# Initialize the level sensor board for 5 capacitance measurement
	# Returns:
	# 	ans - response from help request
	def InitializeUti(self):
		self.SER_OBJ.write('@')
		self.SER_OBJ.write('H')
		ans = self.SER_OBJ.read(1500)
		self.SER_OBJ.write(self.UTI_MODE)
		print self.UTI_MODE
		return ans
		
	# Disconnect serial port object from port
	def SerialDisconnect(self):
		self.SER_OBJ.close()

	# Log UTI measurements to CSV file of given naming convention
	# Arguments:
	#	vals - array of values for measurements from UTI (size=N_MEAS)
	def LogRawValuesCsv(self, vals):
		date_str = time.strftime("%Y-%m-%d")
		time_str = time.strftime("%H:%M:%S")
		filename = self.DATA_PATH + 'ls_value_log_' + date_str + '.csv'
		val_str = time_str
		for i in n.arange(self.N_MEAS):
			val_str = val_str + ',' + str(vals[i])
		f = open(filename,'a')
		f.write(val_str+'\n')
		f.close()
		
	# Log capacitance values to CSV file of given naming convention
	# Arguments:
	#	vals - array of values for measurements from UTI (size=N_SENSORS)
	def LogCapValuesCsv(self, vals):
		date_str = time.strftime("%Y-%m-%d")
		time_str = time.strftime("%H:%M:%S")
		filename = self.DATA_PATH + 'ls_value_log_' + date_str + '.csv'
		val_str = time_str
		for i in n.arange(self.N_SENSORS):
			val_str = val_str + ',' + str(vals[i])
		f = open(filename,'a')
		f.write(val_str+'\n')
		f.close()
		
	# Log UTI measurements to binary file of given naming convention
	# Arguments:
	#	vals - array of values for measurements from UTI (size=N_MEAS)
	def LogRawValuesBin(self, vals):
		unix_time = n.double(time.time())
		date_str = time.strftime("%Y-%m-%d")
		filename = self.DATA_PATH + 'ls_value_log_' + date_str + '.bin'
		f = open(filename,'ab')
		unix_time.tofile(f)
		for i in n.arange(self.N_MEAS):
			val = n.uint32(vals[i])
			val.tofile(f)
		f.close()
		
	# Log capacitance values to binary file of given naming convention
	# Arguments:
	#	vals - array of values for measurements from UTI (size=N_SENSORS)
	def LogCapValuesBin(self, vals):
		unix_time = n.double(time.time())
		date_str = time.strftime("%Y-%m-%d")
		filename = self.DATA_PATH + 'ls_value_log_' + date_str + '.bin'
		f = open(filename,'ab')
		unix_time.tofile(f)
		for i in n.arange(self.N_SENSORS):
			val = n.double(vals[i])
			val.tofile(f)
		f.close()
		
	# Request a measurement from the board, save to log file
	# Returns:
	# 	int_vals - the capacitance measurement of three channels, in integer form
	def PollUtiVals(self):
		try:
			self.SER_OBJ.write('m')
			answer = self.SER_OBJ.read(self.N_MEAS*7+2)
			# print answer
			str_vals = answer.split(' ',self.N_MEAS+1)
			int_vals = n.zeros(self.N_MEAS)
			for i in n.arange(self.N_MEAS):
				if str_vals[i] == '': return n.zeros(self.N_MEAS)
				int_vals[i] = int(str_vals[i],16)
			# self.LogRawValuesCsv(int_vals)
			return int_vals
		except serial.serialutil.SerialException:
			print 'Serial connection error, check UTI'
			quit()
			
		
		
	# Convert the reading from UTI board into N_SENSORS capacitance readings
	# Arguments:
	#	int_vals - array with N_MEAS entries in decimal from UTI reading
	# Returns:
	#	cap_vals - array with N_SENSORS entries in units of capacitance
	def CalculateCapacitance(self, int_vals):
		if (int_vals == n.zeros(self.N_MEAS)).all(): return n.zeros(self.N_SENSORS)
		cap_vals = n.zeros(self.N_SENSORS)
		C_BA = int_vals[0]
		C_CA = int_vals[1]
		# C_DA = int_vals[2]
		# C_EA = int_vals[3]
		# C_FA = int_vals[4]
		
		for i in n.arange(self.N_SENSORS):
			this_cap = int_vals[i+2]
			ratio = float(this_cap - C_BA)/float(C_CA-C_BA)
			cap_vals[i] = self.REF_CAP * ratio
			
		# self.LogCapValuesCsv(cap_vals)
		return cap_vals
		
			
	def __init__(self, port_num):
		self.COM_NUM = port_num
		self.SER_OBJ = self.SerialConnect('COM'+str(port_num))
		# self.initialize_ls()