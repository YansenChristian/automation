

uniqueTaskIds = {}


def Run(projectId, tasks):
    global uniqueTaskIds
    uniqueTaskIds = {}

    filteredTasks = list(filter(lambda task: filterTask(task, projectId), tasks))
    totalTasks = len(filteredTasks)
    completedTasks = list(filter(lambda task: task['completed'] is True, filteredTasks))
    totalCompletedTasks = len(completedTasks)

    if totalTasks == 0:
        return float(0)
    return float(totalCompletedTasks) / float(totalTasks) * 100


def filterTask(task, projectId):
    global uniqueTaskIds
    if ('id' not in task) \
            or ('priority_heading_id' not in task) \
            or ('num_subtasks' not in task) \
            or ('is_milestone' not in task) \
            or ('completed' not in task) \
            or (task['priority_heading_id'] != projectId) \
            or (task['num_subtasks'] != "") \
            or (task['is_milestone'] != ""):
        return False

    if task['id'] in uniqueTaskIds:
        return False

    uniqueTaskIds[task['id']] = True
    return True
