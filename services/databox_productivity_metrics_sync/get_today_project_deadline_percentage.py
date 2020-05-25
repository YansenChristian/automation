import utilities.datetime as DatetimeHelper
from datetime import datetime


def Run(projectId, tasks):
    filteredTasks = list(filter(lambda task: filterTask(task, projectId), tasks))
    if len(filteredTasks) < 1:
        return float(0)

    todayDate = datetime.strptime(DatetimeHelper.getTodayDateInStringFormat('%Y-%m-%d'), '%Y-%m-%d')
    startDate, dueDate = getStartDateAndDueDate(filteredTasks)

    if todayDate < startDate or ((todayDate == startDate) and (startDate != dueDate)):
        return float(0)

    if ((todayDate == startDate) and (startDate == dueDate)) or todayDate >= dueDate:
        return float(100)

    taskWorkingDays = (dueDate - startDate).days + 1
    daysSpent = (todayDate - startDate).days + 1

    return float(daysSpent) / float(taskWorkingDays) * 100


def getStartDateAndDueDate(filteredTasks):
    earliestStartDate = datetime.strptime(filteredTasks[0]['start'], '%Y-%m-%d')
    latestDueDate = datetime.strptime(filteredTasks[0]['due'], '%Y-%m-%d')
    for task in filteredTasks:
        taskStartDate = datetime.strptime(task['start'], '%Y-%m-%d')
        taskDueDate = datetime.strptime(task['due'], '%Y-%m-%d')
        if taskStartDate < earliestStartDate:
            earliestStartDate = taskStartDate
        if taskDueDate > latestDueDate:
            latestDueDate = taskDueDate
    return earliestStartDate, latestDueDate


def filterTask(task, projectId):
    if ('id' not in task) \
            or ('start' not in task) \
            or ('due' not in task) \
            or ('priority_heading_id' not in task) \
            or (task['priority_heading_id'] != projectId) \
            or (task['start'] == "") \
            or (task['due'] == ""):
        return False
    return True

