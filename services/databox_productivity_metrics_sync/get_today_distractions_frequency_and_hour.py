import utilities.datetime as DatetimeHelper
import constants.google_calendar
from datetime import datetime
from utilities.google_calendar_client import getGoogleCalendarClient


def Run():
    todayDate = DatetimeHelper.getTodayDateInStringFormat("%Y-%m-%d")
    beginningOfDayPostfix = "T00:00:00Z"
    endOfDayPostfix = "T23:59:59Z"

    googleCalendarClient = getGoogleCalendarClient()
    result = googleCalendarClient.getEventsForDatetimeRange(
        constants.google_calendar.CALENDARS['Distractions']['id'],
        todayDate + beginningOfDayPostfix,
        todayDate + endOfDayPostfix
    )

    return len(result['items']), calculateTotalDistractionHours(result['items'])


def calculateTotalDistractionHours(distractions):
    totalHours = float(0)
    for event in distractions:
        startDatetime = datetime.fromisoformat(event['start']['dateTime'])
        endDatetime = datetime.fromisoformat(event['end']['dateTime'])
        totalHours += (endDatetime - startDatetime).seconds / 3600
    return totalHours
