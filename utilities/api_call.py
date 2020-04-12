import requests

class ApiCallHelper:
	baseApiUrl = ""
	headers = {}

	def __init__(self, baseApiUrl, baseHeaders):
		self.baseApiUrl = baseApiUrl
		self.headers = baseHeaders

	def toQueryString(self, dictionary):
		queryString = "?"

		dictionaryItemCount = len(dictionary)
		dictionaryPosition = 1
		for key, value in dictionary.items():
			queryString += str(key) + "=" + str(value)
			if(dictionaryPosition != dictionaryItemCount):
				queryString += "&"
			dictionaryPosition += 1
		return queryString

	def getMergedHeaders(self, headers):
		for key, value in self.headers.items():
			headers[key] = value
		return headers

	def sendGet(self, uri, queryString = {}, headers = {}):
		return requests.get(self.baseApiUrl + uri + self.toQueryString(queryString),
			headers=self.getMergedHeaders(headers)).json()

	def sendPost(self, uri, body, queryString = {}, headers = {}):
		return requests.post(self.baseApiUrl + uri + self.toQueryString(queryString),
			data=body,
			headers=self.getMergedHeaders(headers)).json()

	def sendPatch(self, uri, body, queryString = {}, headers = {}):
		return requests.patch(self.baseApiUrl + uri + self.toQueryString(queryString),
			data=body,
			headers=self.getMergedHeaders(headers)).json()
