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
		tasks = zapierStorageClient.get(todayDate +"[TotalTasks]")

		tasks = tasks if tasks is not None else {}
		tasks[payloads['task_gid']] = True
		data = zapierStorageClient.set(todayDate +"[TotalTasks]", tasks)

		return response.returnData(200, data)


class IncreaseTodayCompletedTasksCounterByOne(Resource):
	def post(self):
		parser = reqparse.RequestParser()
		parser.add_argument('task_gid', type=str)
		payloads = parser.parse_args()

		todayDate = DatetimeHelper.getTodayDateInFormat("%Y-%m-%d")
		zapierStorageClient = getZapierStorageClient()
		tasks = zapierStorageClient.get(todayDate +"[CompletedTasks]")

		tasks = tasks if tasks is not None else {}
		tasks[payloads['task_gid']] = True
		data = zapierStorageClient.set(todayDate +"[CompletedTasks]", tasks)

		return response.returnData(200, data)