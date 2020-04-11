from utilities.api_call import ApiCallHelper
import utilities.datetime as DatetimeHelper

class AsanaClient:
	apiUrl = "https://app.asana.com/api/1.0"
	headers = {}
	apiClient = None

	def __init__(self):
		self.headers['Authorization'] = "Bearer 1/1141003277205677:a103bfc476557c49a672e6e4b828978f"
		self.apiClient = ApiCallHelper(self.apiUrl, self.headers)

	def getTodayTasksFromProject(self, projectId):
		uri = "/tasks"
		queryString = {
			"project" : projectId,
			"opt_fields" : "due_on",
			"completed_since" : "now"
		}
		result = self.apiClient.sendGet(uri, queryString)
		if 'errors' in result:
			raise Exception(result['errors'])

		todayDate = DatetimeHelper.getTodayDateInFormat("%Y-%m-%d")
		return list(filter(lambda task: task['due_on'] == todayDate, result['data']))

	def moveTodayTasksAcrossProjects(self, sourceProjectId, destinationProjectId, destinationSectionId):
		def prepareBatchActions(sourceProjectId, destinationProjectId,destinationSectionId):
			actions = []
			todayTasks = self.getTodayTasksFromProject(sourceProjectId)

			for task in todayTasks:
				actions.append({
					"relative_path": "/tasks/" + str(task['gid']) + "/addProject",
					"method": "post",
					"data": {
						"project": destinationProjectId,
						"section": destinationSectionId
					}
				})
			return actions

		uri = "/batch"
		body = {
			"data": {
				"actions": prepareBatchActions(
					sourceProjectId,
					destinationProjectId,
					destinationSectionId
				)
			}
		}

		result = self.apiClient.sendPost(uri, body)
		if 'errors' in result:
			raise Exception(result['errors'])
		return result

AsanaClientInstance = None
def getAsanaClient():
	global AsanaClientInstance
	if AsanaClientInstance == None:
		AsanaClientInstance = AsanaClient()
	return AsanaClientInstance