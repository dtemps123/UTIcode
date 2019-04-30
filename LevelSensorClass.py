import UtiClass as UTI
import numpy as n
import time
import os.path

class LevelSensors:
	# What type of data files do you want to save to {'csv', 'bin'}
	DATA_FORMAT = 'csv'
	def set_DATA_FORMAT(self, fmt):
		if (fmt=='csv' or fmt=='bin'):
			self.DATA_FORMAT = fmt
		else:
			self.DATA_FORMAT = 'csv'
	def get_DATA_FORMAT(self):
		return self.DATA_FORMAT
		
	# What type of data do you want to save {'raw', 'cap'}
	SAVE_FORMAT = 'cap'
	def set_SAVE_FORMAT(self, fmt):
		if (fmt=='cap' or fmt=='raw'):
			self.SAVE_FORMAT = fmt
		else:
			self.SAVE_FORMAT = 'cap'
	def get_SAVE_FORMAT(self):
		return self.SAVE_FORMAT
		
	# Delay between successive measurements of LS (in seconds)
	DELAY_STEP = 10
	def set_DELAY_STEP(self, dly):
		self.DELAY_STEP = dly
	def get_DELAY_STEP(self):
		return self.DELAY_STEP
		

	def __init__(self, uti_port):
		self.UTI_OBJ = UTI.Uti(uti_port)
		self.UTI_OBJ.InitializeUti()
		self.UTI_OBJ.set_REF_CAP(1.28)
		# self.UTI_OBJ.set_DATA_PATH('C:\\Users\\Dylan\\Google Drive\\Research\\XENA-FOXe\\Level Sensors\\data\\')
		
	def MakeLogDecision(self, raw_vals, cap_vals):
		if(self.SAVE_FORMAT=='cap'):
			if(self.DATA_FORMAT=='csv'):
				self.UTI_OBJ.LogCapValuesCsv(cap_vals)
			elif(self.DATA_FORMAT=='bin'):
				self.InitializeBinaryFiles()
				self.UTI_OBJ.LogCapValuesBin(cap_vals)
			else: return
		
		elif(self.SAVE_FORMAT=='raw'):
			if(self.DATA_FORMAT=='csv'):
				self.UTI_OBJ.LogRawValuesCsv(raw_vals)
			elif(self.DATA_FORMAT=='bin'):
				self.InitializeBinaryFiles()
				self.UTI_OBJ.LogRawValuesBin(raw_vals)
			else: return
		
		else: return
		
	def InitializeBinaryFiles(self):
		if self.DATA_FORMAT != 'bin': return
		
		endianflag = n.uint32(0x01020304)
		data_type_id = n.int32(0)
		date_str = time.strftime("%Y-%m-%d")
		filename = self.UTI_OBJ.get_DATA_PATH() + 'ls_value_log_' + date_str + '.bin'
		
		if ( not os.path.isfile(filename) ):
			# make header string
			header = ''
			if (self.SAVE_FORMAT == 'raw'):
				header = 'time;double;1;'
				for i in n.array(['B','C','D','E','F']):
					header = header+'C'+i+'A;uint32;1;'
			elif (self.SAVE_FORMAT == 'cap'):
				header = 'time;double;1'
				for i in n.array(['1','2','3']):
					header = header+'LS'+i+';double;1;'
			else:
				header = 'time;double;1'
				for i in n.array(['B','C','D','E','F']):
					header = header+'C'+i+'A;int32;1;'
			
			head_len = n.uint16(len(header))
			
			fid = open(filename, 'wb')
			endianflag.tofile(fid)
			head_len.tofile(fid)
			fid.write(header.encode('ascii'))
			data_type_id.tofile(fid)
			fid.close()
			
	def MakeOneMeasurement(self):
		raw_vals = self.UTI_OBJ.PollUtiVals()
		cap_vals = self.UTI_OBJ.CalculateCapacitance(raw_vals)
		self.MakeLogDecision(raw_vals, cap_vals)
		print raw_vals
		print cap_vals
		
	def MakeNumMeasurements(self, n_meas):
		self.UTI_OBJ.InitializeUti()
		for i in n.arange(n_meas):
			raw_vals = self.UTI_OBJ.PollUtiVals()
			cap_vals = self.UTI_OBJ.CalculateCapacitance(raw_vals)
			self.MakeLogDecision(raw_vals, cap_vals)
			print raw_vals
			print cap_vals
			# time.sleep(self.DELAY_STEP)
		self.UTI_OBJ.SerialDisconnect()
		
	def MakeInfMeasurements(self):
		self.UTI_OBJ.InitializeUti()
		while True:
			raw_vals = self.UTI_OBJ.PollUtiVals()
			cap_vals = self.UTI_OBJ.CalculateCapacitance(raw_vals)
			self.MakeLogDecision(raw_vals, cap_vals)
			print raw_vals
			print cap_vals
			time.sleep(self.DELAY_STEP)
		