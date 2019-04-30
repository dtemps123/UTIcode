import LevelSensorClass as LS

COMport = 6
MyLs = LS.LevelSensors(COMport)
MyLs.UTI_OBJ.set_DATA_PATH('Z:\\Xelda\\xelda-slow-control-data\\XELDA Level Sensors\\data\\')
MyLs.set_SAVE_FORMAT('raw') #{'raw', 'cap'}
MyLs.set_DATA_FORMAT('bin') #{'bin', 'csv'}
MyLs.set_DELAY_STEP(0.001)
MyLs.InitializeBinaryFiles()
MyLs.MakeNumMeasurements(1000)
