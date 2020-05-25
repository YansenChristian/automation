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
		if result is None:
			return {}
		return result.json()

	def get(self, key):
		queryString = {
			"key": key
		}
		result = self.apiClient.sendGet("", queryString)
		if (result is None) or (key not in result):
			return None
		return result[key]

	def getBulk(self, keys):
		queryString = {
			"key[]": keys
		}
		result = self.apiClient.sendGet("", queryString)
		if result is None:
			return {}
		return result.json()

	def set(self, key, value):
		body = {
			key: value
		}
		result = self.apiClient.sendPost("", json.dumps(body))
		if result is None:
			return {}
		return result.json()

	def setBulk(self, data):
		result = self.apiClient.sendPost("", json.dumps(data))
		if result is None:
			return {}
		return result.json()

	def unset(self, key):
		body = {
			key: None
		}
		result = self.apiClient.sendPost("", json.dumps(body))
		if result is None:
			return {}
		return result.json()

	def unsetBulk(self, *keys):
		body = {}
		for key in keys:
			body[key] = None
		result = self.apiClient.sendPost("", json.dumps(body))
		if result is None:
			return {}
		return result.json()

	def increaseValue(self, key, amount):
		body = {
			'action': 'increment_by',
			'data': {
				'key': key,
				'amount': amount
			}
		}
		result = self.apiClient.sendPatch("", json.dumps(body))
		if result is None:
			return {}
		return result.json()

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
