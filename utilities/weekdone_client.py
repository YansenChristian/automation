from utilities.api_call import ApiCallHelper


class WeekdoneClient:
    apiUrl = "https://api.weekdone.com/1"
    oauthUrl = "https://weekdone.com"
    apiClient = None
    oauthClient = None
    oauthVariables = {
        'access_token': '',
        'refresh_token': 'eyJ2ZXJzaW9uIjoxLCJjbGllbnRfaWQiOjY0OSwidXNlcl9pZCI6MTEwNDY5MSwiaGFzaCI6ImZVT2VSOHRVNU9MU2pQSDREbjZOcmN6OWpnMXlkWnJ0VWdITHBiRnUwcW1qZzRuVXN1SFVIaDMweDV6TCJ9',
        'client_id': '649',
        'client_secret': '420a866112405e42643f83f424af304dfd588988',
        'redirect_uri': '/'
    }

    def __init__(self):
        self.oauthClient = ApiCallHelper(self.oauthUrl, {})
        self.apiClient = ApiCallHelper(self.apiUrl, {})
        self.refreshAccessToken()

    def refreshAccessToken(self):
        uri = "/oauth_token"
        body = {
            'refresh_token': self.oauthVariables['refresh_token'],
            'grant_type': 'refresh_token',
            'client_id': self.oauthVariables['client_id'],
            'client_secret': self.oauthVariables['client_secret'],
            'redirect_uri': self.oauthVariables['redirect_uri']
        }

        result = self.oauthClient.sendPost(uri, body)
        if 'status' in result and result['status'] == "error":
            raise Exception(result)
        self.oauthVariables['access_token'] = result['access_token']

    def updateKeyResultProgress(self, objectiveId, keyResultId, progress):
        uri = "/objective/" + str(objectiveId) + "/result/" + str(keyResultId)
        queryString = {
            'token': self.oauthVariables['access_token']
        }
        body = {
            'progress': int(progress)
        }

        result = self.apiClient.sendPost(uri, body, queryString)
        if result['status'] == "error":
            raise Exception(result)
        return result


WeekdoneClientInstance = None
def getWeekDoneClient():
    global WeekdoneClientInstance
    if WeekdoneClientInstance == None:
        WeekdoneClientInstance = WeekdoneClient()
    return WeekdoneClientInstance
