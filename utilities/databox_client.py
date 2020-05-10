from databox import Client

DataboxClientInstance = None
def getDataboxClient():
	global DataboxClientInstance
	if DataboxClientInstance is None:
		DataboxClientInstance = Client('k2kirto2l6jfcap29sroae')
	return DataboxClientInstance
