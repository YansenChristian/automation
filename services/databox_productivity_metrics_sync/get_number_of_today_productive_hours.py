import utilities.datetime as DatetimeHelper
import constants.google_calendar
from datetime import datetime
from utilities.logger import getLogger
from utilities.api_clients.google_calendar_client import getGoogleCalendarClient


logTagGetNumberOfTodayProductiveHours = "[Get Number of Today Productive Hours]"


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
    response = None
    try:
        response = googleCalendarClient.getEventsForDatetimeRange(
            constants.google_calendar.CALENDARS['Daily Tasks']['id'],
            todayDate + beginningOfDayPostfix,
            todayDate + endOfDayPostfix
        )
    except Exception as error:
        getLogger().error(
            logTagGetNumberOfTodayProductiveHours + " failed to update 'TotalTasks' counter in Zapier Storage",
            error
        )

    return [] if response is None else response['items']
