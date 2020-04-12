from utilities.api_call import ApiCallHelper
import json
import os


class ZapierStorageClient:
	apiUrl = "https://store.zapier.com/api/records"
	headers = {}
	apiClient = None

	def __init__(self):
		self.headers['X-Secret'] = os.getenv("ZAPIER_STORAGE_SECRET")
		self.apiClient = ApiCallHelper(self.apiUrl, self.headers)

	def get(self, key):
		queryString = {
			"key": key
		}
		result = self.apiClient.sendGet("", queryString)
		return result[key] if key in result else None

	def set(self, key, value):
		body = {
			key: value
		}
		return self.apiClient.sendPost("", json.dumps(body))

	def setBulk(self, data):
		return self.apiClient.sendPost("", json.dumps(data))

	def unset(self, key):
		body = {
			key: None
		}
		return self.apiClient.sendPost("", json.dumps(body))

	def unsetBulk(self, *keys):
		body = {}
		for key in keys:
			body[key] = None
		return self.apiClient.sendPost("", json.dumps(body))


ZapierStorageClientInstance = None
def getZapierStorageClient():
	global ZapierStorageClientInstance
	if ZapierStorageClientInstance is None:
		ZapierStorageClientInstance = ZapierStorageClient()
	return ZapierStorageClientInstance
