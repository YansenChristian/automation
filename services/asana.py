import utilities.datetime as DatetimeHelper
from utilities.logger import getLogger
from utilities.api_clients.zapier_storage_client import getZapierStorageClient
from utilities.api_clients.asana_client import getAsanaClient


logTagMoveTodayTasksAcrossProjects = "[Move Today Task Across Projects]"


def moveTodayTasksAcrossProjects(sourceProjectId, destinationProjectId, destinationSectionId):
	results = []
	asanaClient = getAsanaClient()
	try:
		todayTasks = asanaClient.getTasksFromProject(sourceProjectId, True)
	except Exception as error:
		getLogger().error(
			logTagMoveTodayTasksAcrossProjects + " failed to get tasks from project {:s} in Asana".format(sourceProjectId),
			error
		)
		return results

	def prepareBatchActionsForAddingProjectToTasks(todayTasks, destinationProjectId, destinationSectionId):
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
	todayDateString = DatetimeHelper.getTodayDateInStringFormat("%Y-%m-%d")
	todayTaskGids = [task['gid'] for task in todayTasks]
	try:
		results.append(zapierStorageClient.appendUniqueValuesToKey(todayDateString + "[TotalTasks]", todayTaskGids))
	except Exception as error:
		getLogger().error(
			logTagMoveTodayTasksAcrossProjects + " failed to update 'TotalTasks' counter in Zapier Storage",
			error
		)
		return results

	return results
