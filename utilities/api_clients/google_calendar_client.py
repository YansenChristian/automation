import json
import os
import utilities.api_clients.api_call as ApiCallUtil


class GoogleCalendarClient:
    apiUrl = "https://www.googleapis.com"
    oauthUrl = "https://oauth2.googleapis.com"
    apiClient = None
    oauthClient = None

    def __init__(self):
        self.oauthClient = ApiCallUtil.ApiCallHelper(self.oauthUrl, {})
        self.apiClient = ApiCallUtil.ApiCallHelper(self.apiUrl, {})
        self.__refreshAccessToken()

    def __refreshAccessToken(self):
        uri = "/token"
        queryString = {
            'refresh_token': os.getenv("GOOGLE_CALENDAR_REFRESH_TOKEN"),
            'grant_type': 'refresh_token',
            'client_id': os.getenv("GOOGLE_CLIENT_ID"),
            'client_secret': os.getenv("GOOGLE_CLIENT_SECRET"),
        }

        response = self.oauthClient.sendPost(uri, {}, queryString)
        responseData = {} if not ApiCallUtil.isJson(response.content) else response.json()

        if 'access_token' not in responseData:
            raise Exception("invalid response structure: {:s}".format(str(response.content)))

        if 'error' in responseData:
            raise Exception(responseData['error'])

        self.apiClient.headers['Authorization'] = "Bearer " + responseData['access_token']

    def getEventsForDatetimeRange(self, calendarId, startDatetime, endDatetime):
        uri = "/calendar/v3/calendars/" + calendarId + "/events"
        queryString = {
            'timeMin': startDatetime,
            'timeMax': endDatetime
        }

        response = self.apiClient.sendGet(uri, queryString)
        responseData = {} if not ApiCallUtil.isJson(response.content) else response.json()
        if 'error' in responseData:
            raise Exception(responseData['error'])
        return responseData

    def createEvent(self, calendarId, event):
        uri = "/calendar/v3/calendars/" + calendarId + "/events"

        response = self.apiClient.sendPost(uri, json.dumps(event.toDictionary()))
        responseData = {} if not ApiCallUtil.isJson(response.content) else response.json()
        if 'error' in responseData:
            raise Exception(responseData['error'])
        return responseData


GoogleCalendarClientInstance = None
def getGoogleCalendarClient():
    global GoogleCalendarClientInstance
    if GoogleCalendarClientInstance is None:
        GoogleCalendarClientInstance = GoogleCalendarClient()
    return GoogleCalendarClientInstance
