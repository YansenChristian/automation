import utilities.datetime as DatetimeHelper
import constants.google_calendar
from utilities.google_calendar_client import getGoogleCalendarClient


def Run():
    todayDate = DatetimeHelper.getTodayDateInStringFormat("%Y-%m-%d")
    # %2B is an encoding of `+`
    asiaJakartaTimeZone = "%2B07:00"
    beginningOfDayPostfix = "T00:00:00" + asiaJakartaTimeZone
    endOfDayPostfix = "T23:59:59" + asiaJakartaTimeZone

    googleCalendarClient = getGoogleCalendarClient()
    result = googleCalendarClient.getEventsForDatetimeRange(
        constants.google_calendar.CALENDARS['Distractions']['id'],
        todayDate + beginningOfDayPostfix,
        todayDate + endOfDayPostfix
    )

    return len(result['items'])
