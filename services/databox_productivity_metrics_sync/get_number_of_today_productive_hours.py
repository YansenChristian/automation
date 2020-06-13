import utilities.datetime as DatetimeHelper
import constants.google_calendar
from datetime import datetime
from utilities.google_calendar_client import getGoogleCalendarClient


def Run():
    dailyTasks = getDailyTasksFromGoogleCalendar()
    totalHours = float(0)
    for event in dailyTasks:
        startDatetime = datetime.fromisoformat(event['start']['dateTime'])
        endDatetime = datetime.fromisoformat(event['end']['dateTime'])
        totalHours += (endDatetime - startDatetime).seconds / 3600
    return totalHours


def getDailyTasksFromGoogleCalendar():
    todayDate = DatetimeHelper.getTodayDateInStringFormat("%Y-%m-%d")
    # %2B is an encoding of `+`
    asiaJakartaTimeZone = "%2B07:00"
    beginningOfDayPostfix = "T00:00:00" + asiaJakartaTimeZone
    endOfDayPostfix = "T23:59:59" + asiaJakartaTimeZone

    googleCalendarClient = getGoogleCalendarClient()
    return googleCalendarClient.getEventsForDatetimeRange(
        constants.google_calendar.CALENDARS['Daily Tasks']['id'],
        todayDate + beginningOfDayPostfix,
        todayDate + endOfDayPostfix
    )['items']
