import os
import json
import utilities.datetime as DatetimeUtil
import utilities.api_clients.api_call as ApiCallUtil


class AsanaClient:
    apiUrl = "https://app.asana.com/api/1.0"
    headers = {}
    apiClient = None

    def __init__(self):
        self.headers['Authorization'] = "Bearer " + os.getenv("ASANA_ACCESS_TOKEN")
        self.apiClient = ApiCallUtil.ApiCallHelper(self.apiUrl, self.headers)

    def getTasksFromProject(self, projectId, dueOnToday=False):
        uri = "/tasks"
        queryString = {
            "project": projectId,
            "opt_fields": "due_on",
            "completed_since": "now"
        }
        response = self.apiClient.sendGet(uri, queryString)
        responseData = {} if not ApiCallUtil.isJson(response.content) else response.json()

        if 'errors' in responseData:
            raise Exception(responseData['errors'])

        if 'data' not in responseData:
            raise Exception("invalid response structure: {:s}".format(str(response.content)))

        if not dueOnToday:
            return responseData['data']

        todayDateString = DatetimeUtil.getTodayDateInStringFormat("%Y-%m-%d")
        return list(filter(lambda task: task['due_on'] == todayDateString, responseData['data']))

    def getTasksFromSection(self, sectionId, dueOnToday=False):
        uri = "/sections/" + sectionId + "/tasks"
        queryString = {
            "opt_fields": "due_on,name",
            "completed_since": "now"
        }
        response = self.apiClient.sendGet(uri, queryString)
        responseData = {} if not ApiCallUtil.isJson(response.content) else response.json()

        if 'errors' in responseData:
            raise Exception(responseData['errors'])

        if 'data' not in responseData:
            raise Exception("invalid response structure: {:s}".format(str(response.content)))

        if not dueOnToday:
            return responseData['data']

        todayDateString = DatetimeUtil.getTodayDateInStringFormat("%Y-%m-%d")
        return list(filter(lambda task: task['due_on'] == todayDateString, responseData['data']))

    def sendBatchRequest(self, actions=[]):
        if len(actions) < 1:
            return []

        uri = "/batch"
        body = {
            "data": {
                "actions": actions
            }
        }
        response = self.apiClient.sendPost(uri, json.dumps(body))
        return {} if not ApiCallUtil.isJson(response.content) else response.json()


AsanaClientInstance = None
def getAsanaClient():
    global AsanaClientInstance
    if AsanaClientInstance is None:
        AsanaClientInstance = AsanaClient()
    return AsanaClientInstance
