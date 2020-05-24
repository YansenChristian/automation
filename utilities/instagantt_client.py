from utilities.api_call import ApiCallHelper
import constants.instagantt


class InstaganttClient:
    apiUrl = "https://app.instagantt.com"
    oauthUrl = "https://app.asana.com"
    headers = {}
    oauthHeaders = {}
    apiClient = None
    oauthClient = None

    def __init__(self):
        self.oauthHeaders['Cookie'] = "user=1141003277205677; " \
                                      "auth_token=50f951ca38605b230898d4b859d25587; " \
                                      "ticket=888e17e97434bb2320d096dec49fdb7eae382590b556f130555d0e2d1561dab1;"
        self.apiClient = ApiCallHelper(self.apiUrl, self.headers)
        self.oauthClient = ApiCallHelper(self.oauthUrl, self.oauthHeaders)
        self.__refreshConnectSId()

    def __refreshConnectSId(self):
        uri = "/-/oauth_authorize"
        queryString = {
            'response_type': "code",
            'client_id': "5275785675948",
            'redirect_uri': "https://app.instagantt.com/asana/auth",
        }
        result = self.oauthClient.sendGet(uri, queryString)

        connectSId = result.headers['Set-Cookie']
        self.headers['Cookie'] = connectSId[:connectSId.find(';')]
        return self.headers['Cookie']

    def getAllTasks(self):
        uri = "/projects/" + constants.instagantt.PROJECTS['Overall']['gid'] + "/tasks"
        queryString = {
            'completed_since': '16758797247900'
        }
        result = self.apiClient.sendGet(uri, queryString)
        return result.json()


InstaganttClientInstance = None
def getInstaganttClient():
    global InstaganttClientInstance
    if InstaganttClientInstance is None:
        InstaganttClientInstance = InstaganttClient()
    return InstaganttClientInstance
