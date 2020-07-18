import os
import utilities.api_clients.api_call as ApiCallUtil


class WeekdoneClient:
    apiUrl = "https://api.weekdone.com/1"
    oauthUrl = "https://weekdone.com"
    apiClient = None
    oauthClient = None

    def __init__(self):
        self.oauthClient = ApiCallUtil.ApiCallHelper(self.oauthUrl, {})
        self.apiClient = ApiCallUtil.ApiCallHelper(self.apiUrl, {})
        self.__refreshAccessToken()

    def __refreshAccessToken(self):
        uri = "/oauth_token"
        body = {
            'refresh_token': os.getenv('WEEKDONE_REFRESH_TOKEN'),
            'grant_type': 'refresh_token',
            'client_id': os.getenv('WEEKDONE_CLIENT_ID'),
            'client_secret': os.getenv('WEEKDONE_CLIENT_SECRET'),
            'redirect_uri': os.getenv('WEEKDONE_CLIENT_SECRET'),
        }

        response = self.oauthClient.sendPost(uri, body)
        responseData = {} if not ApiCallUtil.isJson(response.content) else response.json()

        if ('status' in responseData and responseData['status'] == "error") or ('access_token' not in responseData):
            raise Exception(responseData['message'])
        self.apiClient.headers['Authorization'] = responseData['access_token']

    def updateKeyResultProgress(self, objectiveId, keyResultId, progress):
        uri = "/objective/" + str(objectiveId) + "/result/" + str(keyResultId)
        queryString = {
            'token': self.apiClient.headers['Authorization']
        }
        body = {
            'progress': int(progress)
        }

        response = self.apiClient.sendPost(uri, body, queryString)
        responseData = {} if not ApiCallUtil.isJson(response.content) else response.json()
        if 'status' in responseData and responseData['status'] == "error":
            raise Exception(responseData['message'])
        return responseData


WeekdoneClientInstance = None
def getWeekDoneClient():
    global WeekdoneClientInstance
    if WeekdoneClientInstance is None:
        WeekdoneClientInstance = WeekdoneClient()
    return WeekdoneClientInstance
