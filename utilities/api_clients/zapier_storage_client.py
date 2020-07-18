import utilities.api_clients.api_call as ApiCallUtil
import json
import os


class ZapierStorageClient:
	apiUrl = "https://store.zapier.com/api/records"
	headers = {}
	apiClient = None

	def __init__(self):
		self.headers['X-Secret'] = os.getenv("ZAPIER_STORAGE_SECRET")
		self.apiClient = ApiCallUtil.ApiCallHelper(self.apiUrl, self.headers)

	def all(self):
		response = self.apiClient.sendGet("", {})
		return {} if not ApiCallUtil.isJson(response.content) else response.json()

	def get(self, key):
		queryString = {
			"key": key
		}
		response = self.apiClient.sendGet("", queryString)
		responseData = {} if not ApiCallUtil.isJson(response.content) else response.json()
		return None if key not in responseData else responseData[key]

	def getBulk(self, keys):
		queryString = {
			"key[]": keys
		}
		response = self.apiClient.sendGet("", queryString)
		return {} if not ApiCallUtil.isJson(response.content) else response.json()

	def set(self, key, value):
		body = {
			key: value
		}
		response = self.apiClient.sendPost("", json.dumps(body))
		return {} if not ApiCallUtil.isJson(response.content) else response.json()

	def setBulk(self, data):
		response = self.apiClient.sendPost("", json.dumps(data))
		return {} if not ApiCallUtil.isJson(response.content) else response.json()

	def unset(self, key):
		body = {
			key: None
		}
		result = self.apiClient.sendPost("", json.dumps(body))
		return {} if not ApiCallUtil.isJson(response.content) else response.json()

	def unsetBulk(self, *keys):
		body = {}
		for key in keys:
			body[key] = None
		response = self.apiClient.sendPost("", json.dumps(body))
		return {} if not ApiCallUtil.isJson(response.content) else response.json()

	def increaseValue(self, key, amount):
		body = {
			'action': 'increment_by',
			'data': {
				'key': key,
				'amount': amount
			}
		}
		response = self.apiClient.sendPatch("", json.dumps(body))
		return {} if not ApiCallUtil.isJson(response.content) else response.json()

	def appendUniqueValuesToKey(self, key, values = []):
		if len(values) < 1:
			return []
		data = self.get(key)
		data = {} if data is None else data
		for value in values:
			data[value] = True
		return self.set(key, data)


ZapierStorageClientInstance = None
def getZapierStorageClient():
	global ZapierStorageClientInstance
	if ZapierStorageClientInstance is None:
		ZapierStorageClientInstance = ZapierStorageClient()
	return ZapierStorageClientInstance
