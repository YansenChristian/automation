import os
from utilities.api_call import ApiCallHelper


class WeekdoneClient:
    apiUrl = "https://api.weekdone.com/1"
    oauthUrl = "https://weekdone.com"
    apiClient = None
    oauthClient = None

    def __init__(self):
        self.oauthClient = ApiCallHelper(self.oauthUrl, {})
        self.apiClient = ApiCallHelper(self.apiUrl, {})
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

        result = self.oauthClient.sendPost(uri, body)
        if result is None:
            raise Exception("Failed to refresh weekdone's access token")

        responseData = result.json()
        if ('status' in responseData and responseData['status'] == "error") or ('access_token' not in responseData):
            raise Exception(responseData)
        self.apiClient.headers['Authorization'] = responseData['access_token']

    def updateKeyResultProgress(self, objectiveId, keyResultId, progress):
        uri = "/objective/" + str(objectiveId) + "/result/" + str(keyResultId)
        queryString = {
            'token': self.apiClient.headers['Authorization']
        }
        body = {
            'progress': int(progress)
        }

        result = self.apiClient.sendPost(uri, body, queryString)
        if result is None:
            raise Exception("Failed to refresh weekdone's access token")

        responseData = result.json()
        if 'status' in responseData and responseData['status'] == "error":
            raise Exception(responseData)
        return responseData


WeekdoneClientInstance = None
def getWeekDoneClient():
    global WeekdoneClientInstance
    if WeekdoneClientInstance is None:
        WeekdoneClientInstance = WeekdoneClient()
    return WeekdoneClientInstance
