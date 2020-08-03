import constants.asana
import services.common.asana as AsanaService


def Run(tasks):
    overviewProjectId = constants.asana.PROJECTS['Overview']['gid']
    inProgressSectionId = constants.asana.PROJECTS['Overview']['sections']['In Progress']['gid']
    return AsanaService.moveTasksToProjectSection(tasks, overviewProjectId, inProgressSectionId)
