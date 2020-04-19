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

	def all(self):
		result = self.apiClient.sendGet("", {})
		return result

	def get(self, key):
		queryString = {
			"key": key
		}
		result = self.apiClient.sendGet("", queryString)
		return result[key] if key in result else None

	def getBulk(self, keys):
		queryString = {
			"key[]": keys
		}
		result = self.apiClient.sendGet("", queryString)
		return result

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

	def increaseValue(self, key, amount):
		body = {
			'action': 'increment_by',
			'data': {
				'key': key,
				'amount': amount
			}
		}
		return self.apiClient.sendPatch("", json.dumps(body))

	def appendUniqueValuesToKey(self, key, values = []):
		if len(values) < 1:
			return []
		data = self.get(key)
		data = data if data is not None else {}
		for value in values:
			data[value] = True
		return self.set(key, data)




ZapierStorageClientInstance = None
def getZapierStorageClient():
	global ZapierStorageClientInstance
	if ZapierStorageClientInstance is None:
		ZapierStorageClientInstance = ZapierStorageClient()
	return ZapierStorageClientInstance
