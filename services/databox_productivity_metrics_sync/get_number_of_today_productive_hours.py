from datetime import datetime
import utilities.datetime as DatetimeHelper


def Run(tasks, numberOfDistractionsHour):
    filteredTasks = list(filter(filterTask, tasks))
    numberOfTasksHour = calculateTodayTasksHour(filteredTasks)
    return numberOfTasksHour - float(numberOfDistractionsHour)


def calculateTodayTasksHour(filteredTasks):
    numberOfTodayTasksHour = float(0)
    for task in filteredTasks:
        startDate = datetime.strptime(task['start'], '%Y-%m-%d')
        dueDate = datetime.strptime(task['due'], '%Y-%m-%d')

        workingDays = (dueDate - startDate).days + 1
        estimatedHours = task['estimated_hours'] if task['estimated_hours'] != "" else 0
        numberOfTodayTasksHour += (float(estimatedHours) / 100) / float(workingDays)
    return numberOfTodayTasksHour


def filterTask(task):
    if ('type' in task) \
            or ('start' not in task) \
            or ('due' not in task) \
            or ('completed' not in task) \
            or ('estimated_hours' not in task) \
            or ('is_milestone' not in task) \
            or (task['start'] == "") \
            or (task['due'] == "") \
            or (task['is_milestone'] != ""):
        return False

    todayDate = datetime.strptime(DatetimeHelper.getTodayDateInStringFormat('%Y-%m-%d'), '%Y-%m-%d')
    startDate = datetime.strptime(task['start'], '%Y-%m-%d')
    dueDate = datetime.strptime(task['due'], '%Y-%m-%d')

    if (todayDate < startDate) or (todayDate > dueDate):
        return False

    if (dueDate == todayDate) and (task['completed'] == ""):
        return False
    return True
