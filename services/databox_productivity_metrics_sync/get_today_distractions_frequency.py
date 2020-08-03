import utilities.datetime as DatetimeHelper
import constants.google_calendar
from utilities.logger import getLogger
from utilities.api_clients.google_calendar_client import getGoogleCalendarClient


logTagGetTodayDistractionFrequency = "[Get Today Distraction Frequency]"


def Run():
    todayDate = DatetimeHelper.getTodayDateInStringFormat("%Y-%m-%d")
    # %2B is an encoding of `+`
    asiaJakartaTimeZone = "%2B07:00"
    beginningOfDayPostfix = "T00:00:00" + asiaJakartaTimeZone
    endOfDayPostfix = "T23:59:59" + asiaJakartaTimeZone

    googleCalendarClient = getGoogleCalendarClient()
    try:
        result = googleCalendarClient.getEventsForDatetimeRange(
            constants.google_calendar.CALENDARS['Distractions']['id'],
            todayDate + beginningOfDayPostfix,
            todayDate + endOfDayPostfix
        )
        if 'items' not in result:
            raise Exception("invalid response structure")

    except Exception as error:
        getLogger().error(
            logTagGetTodayDistractionFrequency + " failed to get events 'Distractions' from Google Calendar",
            error
        )
        raise error

    return len(result['items'])
