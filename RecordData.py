import LevelSensorClass as LS

COMport = 6
MyLs = LS.LevelSensors(COMport)
MyLs.UTI_OBJ.set_DATA_PATH('C:\\Path\\to\\data\\')
MyLs.set_SAVE_FORMAT('raw') #{'raw', 'cap'}
MyLs.set_DATA_FORMAT('bin') #{'bin', 'csv'}
MyLs.set_DELAY_STEP(0.001)
MyLs.InitializeBinaryFiles()

# This will take 1000 measurements
MyLs.MakeNumMeasurements(1000)

# Uncomment this to make only one measurement at a time
# MyLs.MakeOneMeasurement()

# Uncomment this to make infinite measurements until Ctrl+C is given in command line
# MyLs.MakeInfMeasurements()

