import datetime
import constants.google_calendar
import models.google_calendar
from utilities.api_clients.google_calendar_client import getGoogleCalendarClient
from utilities.logger import getLogger


logTagCreateEventsForEachTasksInGCalendar = "[Create Events For Each Tasks on GCalendar]"


def Run(tasks):
    result = []
    googleCalendarClient = getGoogleCalendarClient()
    try:
        for task in tasks:
            startDatetime = datetime.datetime.now().replace(microsecond=0)
            endDatetime = startDatetime + datetime.timedelta(minutes=calculateDayWorkloadInMinutes(
                task.start,
                task.due,
                0 if task.estimatedHours == "" else task.estimatedHours
            ))

            eventStart = models.google_calendar.EventDate(dateTime=startDatetime.isoformat() + '+07:00', timeZone="Asia/Jakarta")
            eventEnd = models.google_calendar.EventDate(dateTime=endDatetime.isoformat() + '+07:00', timeZone="Asia/Jakarta")
            eventReminder = models.google_calendar.EventReminder(method='popup', minutes=5)
            event = models.google_calendar.Event(
                summary=task.name,
                start=eventStart,
                end=eventEnd,
                reminders=[eventReminder],
            )

            result.append(googleCalendarClient.createEvent(
                calendarId=constants.google_calendar.CALENDARS['Daily Tasks']['id'],
                event=event,
            ))
    except Exception as error:
        getLogger().error(
            logTagCreateEventsForEachTasksInGCalendar + " failed to create events in 'Daily Task' on Google Calendar",
            error
        )
        raise error
    return result


def calculateDayWorkloadInMinutes(startDate, endDate, estimatedHours):
    start = datetime.datetime.strptime(startDate, '%Y-%m-%d')
    end = datetime.datetime.strptime(endDate, '%Y-%m-%d')
    numberOfWorkingDays = (end - start).days + 1
    estimatedMinutes = int((float(estimatedHours) / 100) * 60)
    return estimatedMinutes / numberOfWorkingDays
