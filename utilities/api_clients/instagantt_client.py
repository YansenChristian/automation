import os
import constants.instagantt
import utilities.api_clients.api_call as ApiCallUtil


class InstaganttClient:
    apiUrl = "https://app.instagantt.com"
    oauthUrl = "https://app.asana.com"
    headers = {}
    oauthHeaders = {}
    apiClient = None
    oauthClient = None

    def __init__(self):
        self.oauthHeaders['Cookie'] = "user=" + os.getenv("INSTAGANTT_USER_ID") + "; " \
                                      "auth_token=" + os.getenv("INSTAGANTT_AUTHENTICATION_TOKEN") + "; " \
                                      "ticket=" + os.getenv("INSTAGANTT_TICKET") + ";"
        self.apiClient = ApiCallUtil.ApiCallHelper(self.apiUrl, self.headers)
        self.oauthClient = ApiCallUtil.ApiCallHelper(self.oauthUrl, self.oauthHeaders)
        self.__refreshConnectSId()

    def __refreshConnectSId(self):
        uri = "/-/oauth_authorize"
        queryString = {
            'response_type': "code",
            'client_id': os.getenv("INSTAGANTT_CLIENT_ID"),
            'redirect_uri': "https://app.instagantt.com/asana/auth",
        }
        response = self.oauthClient.sendGet(uri, queryString)
        connectSId = response.headers['Set-Cookie']
        self.headers['Cookie'] = connectSId[:connectSId.find(';')]
        return self.headers['Cookie']

    def getAllTasks(self, withCompletedTask = False):
        uri = "/projects/" + constants.instagantt.CONNECTIONS['Overall']['gid'] + "/tasks"
        queryString = {}
        if not withCompletedTask:
            queryString['completed_since'] = '16758797247900'

        response = self.apiClient.sendGet(uri, queryString)
        return [] if not ApiCallUtil.isJson(response.content) else response.json()


InstaganttClientInstance = None
def getInstaganttClient():
    global InstaganttClientInstance
    if InstaganttClientInstance is None:
        InstaganttClientInstance = InstaganttClient()
    return InstaganttClientInstance
