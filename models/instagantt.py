

class Task:
    def __init__(self, gid, name, start, due, estimatedHours, completed, memberships=[]):
        self.gid = gid
        self.name = name
        self.start = start
        self.due = due
        self.estimatedHours = estimatedHours
        self.completed = completed
        self.memberships = memberships

    def toDictionary(self):
        task = {
            'gid': self.gid,
            'name': self.name,
            'start': self.start,
            'due': self.due,
            'estimatedHours': self.estimatedHours,
            'completed': self.completed,
            'memberships': [],
        }
        try:
            for membership in self.memberships:
                task['memberships'].append(membership.toDictionary())
        except Exception as error:
            raise Exception("task model has invalid field value: " + str(error))
        return task


class TaskMembership:
    def __init__(self, project, section):
        self.project = project
        self.section= section

    def toDictionary(self):
        try:
            membership = {
                'project': self.project.toDictionary(),
                'section': self.section.toDictionary(),
            }
        except Exception as error:
            raise Exception("membership has invalid field value: " + str(error))
        return membership


class TaskMembershipProject:
    def __init__(self, gid, name):
        self.gid = gid
        self.name = name

    def toDictionary(self):
        return {
            'gid': self.gid,
            'name': self.name,
        }


class TaskMembershipSection:
    def __init__(self, gid, name):
        self.gid = gid
        self.name = name

    def toDictionary(self):
        return {
            'gid': self.gid,
            'name': self.name,
        }
