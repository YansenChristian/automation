import os
from utilities.api_call import ApiCallHelper


class GoogleCalendarClient:
    apiUrl = "https://www.googleapis.com"
    oauthUrl = "https://oauth2.googleapis.com"
    apiClient = None
    oauthClient = None

    def __init__(self):
        self.oauthClient = ApiCallHelper(self.oauthUrl, {})
        self.apiClient = ApiCallHelper(self.apiUrl, {})
        self.__refreshAccessToken()

    def __refreshAccessToken(self):
        uri = "/token"
        queryString = {
            'refresh_token': os.getenv("GOOGLE_CALENDAR_REFRESH_TOKEN"),
            'grant_type': 'refresh_token',
            'client_id': os.getenv("GOOGLE_CLIENT_ID"),
            'client_secret': os.getenv("GOOGLE_CLIENT_SECRET"),
        }

        result = self.oauthClient.sendPost(uri, {}, queryString)
        responseData = result.json()
        if 'error' in responseData:
            raise Exception(responseData)
        self.apiClient.headers['Authorization'] = "Bearer " + responseData['access_token']

    def getEventsForDatetimeRange(self, calendarId, startDatetime, endDatetime):
        uri = "/calendar/v3/calendars/" + calendarId + "/events"
        queryString = {
            'timeMin': startDatetime,
            'timeMax': endDatetime
        }

        result = self.apiClient.sendGet(uri, queryString)
        responseData = result.json()
        if 'error' in responseData:
            raise Exception(responseData)
        return responseData


GoogleCalendarClientInstance = None
def getGoogleCalendarClient():
    global GoogleCalendarClientInstance
    if GoogleCalendarClientInstance is None:
        GoogleCalendarClientInstance = GoogleCalendarClient()
    return GoogleCalendarClientInstance
