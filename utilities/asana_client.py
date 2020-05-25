import os
import json
import utilities.datetime as DatetimeHelper
from utilities.api_call import ApiCallHelper


class AsanaClient:
    apiUrl = "https://app.asana.com/api/1.0"
    headers = {}
    apiClient = None

    def __init__(self):
        self.headers['Authorization'] = "Bearer " + os.getenv("ASANA_ACCESS_TOKEN")
        self.apiClient = ApiCallHelper(self.apiUrl, self.headers)

    def getTasksFromProject(self, projectId, dueOnToday=False):
        uri = "/tasks"
        queryString = {
            "project": projectId,
            "opt_fields": "due_on",
            "completed_since": "now"
        }
        result = self.apiClient.sendGet(uri, queryString)
        if (result is None) or ('data' not in result):
            return []

        if 'errors' in result:
            raise Exception(result['errors'])

        if not dueOnToday:
            return result['data']

        todayDateString = DatetimeHelper.getTodayDateInStringFormat("%Y-%m-%d")
        return list(filter(lambda task: task['due_on'] == todayDateString, result['data']))

    def getTasksFromSection(self, sectionId, dueOnToday=False):
        uri = "/sections/" + sectionId + "/tasks"
        queryString = {
            "opt_fields": "due_on,name",
            "completed_since": "now"
        }
        result = self.apiClient.sendGet(uri, queryString)
        if (result is None) or ('data' not in result):
            return []

        if 'errors' in result:
            raise Exception(result['errors'])

        if not dueOnToday:
            return result['data']

        todayDateString = DatetimeHelper.getTodayDateInStringFormat("%Y-%m-%d")
        return list(filter(lambda task: task['due_on'] == todayDateString, result['data']))

    def sendBatchRequest(self, actions=[]):
        if len(actions) < 1:
            return []

        uri = "/batch"
        body = {
            "data": {
                "actions": actions
            }
        }
        result = self.apiClient.sendPost(uri, json.dumps(body))
        if result is None:
            return {}
        return result.json()


AsanaClientInstance = None


def getAsanaClient():
    global AsanaClientInstance
    if AsanaClientInstance is None:
        AsanaClientInstance = AsanaClient()
    return AsanaClientInstance
