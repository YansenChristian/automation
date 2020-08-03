from utilities.api_clients.instagantt_client import getInstaganttClient
import models.instagantt


def getAllTasks():
    client = getInstaganttClient()
    allObjects = client.getAll()

    tasks = []
    for obj in allObjects:
        if 'type' in obj and obj['type'] == 'board':
            continue

        memberships = []
        for membership in obj['memberships']:
            project = models.instagantt.TaskMembershipProject(
                gid= membership['project']['gid'],
                name= membership['project']['name'],
            )
            section = models.instagantt.TaskMembershipSection(
                gid= membership['section']['gid'],
                name= membership['section']['name'],
            )
            memberships.append(models.instagantt.TaskMembership(project, section))

        tasks.append(models.instagantt.Task(
            gid= obj['gid'],
            name= obj['name'],
            start= obj['start'],
            due= obj['due'],
            estimatedHours= obj['estimated_hours'],
            completed= obj['completed'] != "",
            memberships= memberships,
        ))
    return tasks
