import requests
import json
from utilities.logger import getLogger


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
		requestHeader = self.getMergedHeaders(headers)
		response = requests.get(
			url=self.baseApiUrl + uri + self.toQueryString(queryString),
			headers=requestHeader
		)
		getLogger().egress(
			url=self.baseApiUrl + uri,
			method="GET",
			statusCode=response.status_code,
			requestHeader=str(requestHeader),
			requestBody="",
			responseHeader=str(response.headers),
			responseBody=response.content.decode("utf-8")
		)
		return response

	def sendPost(self, uri, body, queryString = {}, headers = {}):
		requestHeader = self.getMergedHeaders(headers)
		response = requests.post(
			url=self.baseApiUrl + uri + self.toQueryString(queryString),
			data=body,
			headers=requestHeader
		)
		getLogger().egress(
			url=self.baseApiUrl + uri,
			method="POST",
			statusCode=response.status_code,
			requestHeader=str(requestHeader),
			requestBody=str(body),
			responseHeader=str(response.headers),
			responseBody=response.content.decode("utf-8")
		)
		return response

	def sendPatch(self, uri, body, queryString = {}, headers = {}):
		requestHeader = self.getMergedHeaders(headers)
		response = requests.patch(
			url=self.baseApiUrl + uri + self.toQueryString(queryString),
			data=body,
			headers=requestHeader
		)
		getLogger().egress(
			url=self.baseApiUrl + uri,
			method="PATCH",
			statusCode=response.status_code,
			requestHeader=str(requestHeader),
			requestBody=str(body),
			responseHeader=str(response.headers),
			responseBody=response.content.decode("utf-8")
		)
		return response


def isJson(responseBody):
	try:
		json.loads(responseBody)
	except ValueError:
		return False
	return True
