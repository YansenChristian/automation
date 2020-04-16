from utilities.zapier_storage_client import getZapierStorageClient
from utilities.asana_client import getAsanaClient
import utilities.datetime as DatetimeHelper


def moveTodayTasksAcrossProjects(sourceProjectId, destinationProjectId, destinationSectionId):
	results = []
	asanaClient = getAsanaClient()
	todayTasks = asanaClient.getTasksFromProject(sourceProjectId, True)
	def prepareBatchActionsForAddingProjectToTasks(todayTasks, destinationProjectId ,destinationSectionId):
		actions = []
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

	actions = prepareBatchActionsForAddingProjectToTasks(todayTasks, destinationProjectId, destinationSectionId)
	results.append(asanaClient.sendBatchRequest(actions))

	zapierStorageClient = getZapierStorageClient()
	todayDate = DatetimeHelper.getTodayDateInFormat("%Y-%m-%d")
	todayTaskGids = [task['gid'] for task in todayTasks]
	results.append(zapierStorageClient.appendUniqueValuesToKey(todayDate + "[TotalTasks]", todayTaskGids))
	return results
