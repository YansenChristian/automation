from utilities.goalify_client import getGoalifyClient
from utilities.weekdone_client import getWeekDoneClient
import constants.goalify
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