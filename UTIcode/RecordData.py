import UTIcode.LevelSensorClass as LS

COMport = 0
MyLs = LS.LevelSensors(COMport)
# MyLs.UTI_OBJ.set_DATA_PATH('C:\\Path\\to\\data\\')	# Note default path is user home directory
MyLs.set_SAVE_FORMAT('cap') #{'raw', 'cap'}
MyLs.set_DATA_FORMAT('csv') #{'bin', 'csv'}
MyLs.set_DELAY_STEP(0.01)
MyLs.InitializeBinaryFiles()

# This will take 1000 measurements
MyLs.MakeNumMeasurements(1000)

# Uncomment this to make only one measurement at a time
# MyLs.MakeOneMeasurement()

# Uncomment this to make infinite measurements until Ctrl+C is given in command line
# MyLs.MakeInfMeasurements()

