from utilities.goalify_client import getGoalifyClient
from utilities.weekdone_client import getWeekDoneClient
from utilities.zapier_storage_client import getZapierStorageClient
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

    weekdoneClient = getWeekDoneClient()
    objectiveId = constants.weekdone.OBJECTIVES['Time Management']['id']
    keyResultId = constants.weekdone.OBJECTIVES['Time Management']['key_results']['Productivity']['id']
    productivity = calculateProductivityPercentage(progress['target'], progress['value'])
    return weekdoneClient.updateKeyResultProgress(objectiveId, keyResultId, productivity)


def syncDisciplineWithGoalify():
    goalifyClient = getGoalifyClient()
    progress = goalifyClient.getGoalProgress(constants.goalify.GOALS['Discipline']['id'])[0]

    weekdoneClient = getWeekDoneClient()
    objectiveId = constants.weekdone.OBJECTIVES['Time Management']['id']
    keyResultId = constants.weekdone.OBJECTIVES['Time Management']['key_results']['Discipline']['id']
    return weekdoneClient.updateKeyResultProgress(objectiveId, keyResultId, progress['achievement'])


def syncCommitmentWithGoalify():
    zapierStorageClient = getZapierStorageClient()
    todayDate = DatetimeHelper.getTodayDateInFormat("%Y-%m-%d")
    totalTasksKey = todayDate+"[TotalTasks]"
    completedTasksKey = todayDate+"[CompletedTasks]"
    data = zapierStorageClient.getBulk([totalTasksKey, completedTasksKey])

    def calculateCommitmentPercentage(numberOfCompletedTasks, totalTasks):
        if totalTasks == 0:
            return 0
        return int(numberOfCompletedTasks / totalTasks * 100)
    numberOfCompletedTasks = len(data[completedTasksKey]) if completedTasksKey in data else 0
    totalTasks = len(data[totalTasksKey]) if totalTasksKey in data else 0

    weekdoneClient = getWeekDoneClient()
    objectiveId = constants.weekdone.OBJECTIVES['Time Management']['id']
    keyResultId = constants.weekdone.OBJECTIVES['Time Management']['key_results']['Commitment']['id']
    commitmentPercentage = calculateCommitmentPercentage(numberOfCompletedTasks, totalTasks)
    return weekdoneClient.updateKeyResultProgress(objectiveId, keyResultId, commitmentPercentage)