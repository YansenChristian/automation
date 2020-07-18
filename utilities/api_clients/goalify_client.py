import os

import utilities.api_clients.api_call as ApiCallUtil


class GoalifyClient:
    apiUrl = "https://g2.goalifyapp.com/api/1.0.1"
    headers = {}
    apiClient = None

    def __init__(self):
        self.headers['Authorization'] = "Bearer " + os.getenv("GOALIFY_ACCESS_TOKEN")
        self.apiClient = ApiCallUtil.ApiCallHelper(self.apiUrl, self.headers)

    def getGoalProgress(self, goalId):
        uri = "/goals/" + goalId
        queryString = {
            'kpi': 'perf_d_1'
        }

        response = self.apiClient.sendGet(uri, queryString)
        responseData = {} if not ApiCallUtil.isJson(response.content) else response.json()
        if ('result' not in responseData) \
                or ('goal' not in responseData['result']) \
                or ('kpi' not in responseData['result']['goal']) \
                or ('perf_d_1' not in responseData['result']['goal']['kpi']):
            raise Exception("invalid response structure: {:s}".format(str(response.content)))
        return responseData['result']['goal']['kpi']['perf_d_1']


GoalifyClientInstance = None
def getGoalifyClient():
    global GoalifyClientInstance
    if GoalifyClientInstance is None:
        GoalifyClientInstance = GoalifyClient()
    return GoalifyClientInstance
