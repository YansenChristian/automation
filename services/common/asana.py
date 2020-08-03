from utilities.logger import getLogger
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
		raise error

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
	return results


def moveTasksToProjectSection(tasks, destinationProjectId, destinationSectionId):
	asanaClient = getAsanaClient()

	def prepareBatchActionsForAddingProjectToTasks(tasks, destinationProjectId, destinationSectionId):
		actions = []
		for task in tasks:
			actions.append({
				"relative_path": "/tasks/" + str(task.gid) + "/addProject",
				"method": "post",
				"data": {
					"project": destinationProjectId,
					"section": destinationSectionId
				}
			})
		return actions

	actions = prepareBatchActionsForAddingProjectToTasks(tasks, destinationProjectId, destinationSectionId)
	return asanaClient.sendBatchRequest(actions)
