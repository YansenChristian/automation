from utilities.goalify_client import getGoalifyClient
from utilities.zapier_storage_client import getZapierStorageClient
from models.databox import Metric
import utilities.datetime as DatetimeHelper
import constants.goalify
import constants.asana
import constants.weekdone


def syncProductivityWithGoalify():
	goalifyClient = getGoalifyClient()
	progress = goalifyClient.getGoalProgress(constants.goalify.GOALS['Productivity']['id'])[0]

	def calculateProductivityPercentage(breakTimeInMinutes, breakTimeSpentInMinutes):
		totalTimeInMinutes = (100 / 35) * breakTimeInMinutes
		return (totalTimeInMinutes - breakTimeSpentInMinutes) / totalTimeInMinutes * 100

	productivityPercentage = calculateProductivityPercentage(progress['target'], progress['value'])
	return Metric("Productivity", productivityPercentage, "%").toDictionary()


def syncDisciplineWithGoalify():
	goalifyClient = getGoalifyClient()
	progress = goalifyClient.getGoalProgress(constants.goalify.GOALS['Discipline']['id'])[0]

	disciplinePercentage = progress['achievement']
	return Metric("Discipline", disciplinePercentage, "%").toDictionary()


def syncCommitmentWithAsana():
	zapierStorageClient = getZapierStorageClient()
	todayDate = DatetimeHelper.getTodayDateInFormat("%Y-%m-%d")
	totalTasksKey = todayDate + "[TotalTasks]"
	completedTasksKey = todayDate + "[CompletedTasks]"
	data = zapierStorageClient.getBulk([totalTasksKey, completedTasksKey])

	def calculateCommitmentPercentage(numberOfCompletedTasks, totalTasks):
		if totalTasks == 0:
			return 0
		return int(numberOfCompletedTasks / totalTasks * 100)

	numberOfCompletedTasks = len(data[completedTasksKey]) if completedTasksKey in data else 0
	totalTasks = len(data[totalTasksKey]) if totalTasksKey in data else 0
	commitmentPercentage = calculateCommitmentPercentage(numberOfCompletedTasks, totalTasks)
	return Metric("Commitment", commitmentPercentage, "%").toDictionary()
