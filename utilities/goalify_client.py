import os

from utilities.api_call import ApiCallHelper


class GoalifyClient:
    apiUrl = "https://g2.goalifyapp.com/api/1.0.1"
    headers = {}
    apiClient = None

    def __init__(self):
        self.headers['Authorization'] = "Bearer " + os.getenv("GOALIFY_ACCESS_TOKEN")
        self.apiClient = ApiCallHelper(self.apiUrl, self.headers)

    def getGoalProgress(self, goalId):
        uri = "/goals/" + goalId
        queryString = {
            'kpi': 'perf_d_1'
        }

        result = self.apiClient.sendGet(uri, queryString)
        if (result is None) \
                or ('result' not in result) \
                or ('goal' not in result['result']) \
                or ('kpi' not in result['result']['goal']) \
                or ('perf_d_1' not in result['result']['goal']['kpi']):
            return []
        return result['result']['goal']['kpi']['perf_d_1']


GoalifyClientInstance = None


def getGoalifyClient():
    global GoalifyClientInstance
    if GoalifyClientInstance is None:
        GoalifyClientInstance = GoalifyClient()
    return GoalifyClientInstance
