import utilities.http_response as response
import utilities.datetime as DatetimeHelper
from utilities.api_clients.zapier_storage_client import getZapierStorageClient
from flask_restful import Resource, reqparse


class IncreaseTodayTasksCounterByOne(Resource):
	def post(self):
		parser = reqparse.RequestParser()
		parser.add_argument('task_gid', type=str)
		payloads = parser.parse_args()

		todayDateString = DatetimeHelper.getTodayDateInStringFormat("%Y-%m-%d")
		zapierStorageClient = getZapierStorageClient()
		result = zapierStorageClient.appendUniqueValuesToKey(todayDateString + "[TotalTasks]", [payloads['task_gid']])
		return response.returnData(200, result)


class IncreaseTodayCompletedTasksCounterByOne(Resource):
	def post(self):
		parser = reqparse.RequestParser()
		parser.add_argument('task_gid', type=str)
		payloads = parser.parse_args()

		todayDateString = DatetimeHelper.getTodayDateInStringFormat("%Y-%m-%d")
		zapierStorageClient = getZapierStorageClient()
		result = zapierStorageClient.appendUniqueValuesToKey(todayDateString + "[CompletedTasks]", [payloads['task_gid']])
		return response.returnData(200, result)
