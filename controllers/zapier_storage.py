import utilities.http_response as response
from utilities.zapier_storage_client import getZapierStorageClient
from flask_restful import Resource, reqparse
import utilities.datetime as DatetimeHelper


class IncreaseTodayTasksCounterByOne(Resource):
	def post(self):
		parser = reqparse.RequestParser()
		parser.add_argument('task_gid', type=str)
		payloads = parser.parse_args()

		todayDate = DatetimeHelper.getTodayDateInFormat("%Y-%m-%d")
		zapierStorageClient = getZapierStorageClient()
		result = zapierStorageClient.appendUniqueValuesToKey(todayDate + "[TotalTasks]", [payloads['task_gid']])
		return response.returnData(200, result)


class IncreaseTodayCompletedTasksCounterByOne(Resource):
	def post(self):
		parser = reqparse.RequestParser()
		parser.add_argument('task_gid', type=str)
		payloads = parser.parse_args()

		todayDate = DatetimeHelper.getTodayDateInFormat("%Y-%m-%d")
		zapierStorageClient = getZapierStorageClient()
		result = zapierStorageClient.appendUniqueValuesToKey(todayDate + "[CompletedTasks]", [payloads['task_gid']])
		return response.returnData(200, result)
