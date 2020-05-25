from databox import Client

DataboxClientInstance = None
def getDataboxClient(token):
	global DataboxClientInstance
	if DataboxClientInstance is None:
		DataboxClientInstance = Client(token)
	return DataboxClientInstance
