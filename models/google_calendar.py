

class Event:
    def __init__(self, summary, start, end, reminders=[]):
        self.summary = summary
        self.start = start
        self.end = end
        self.reminders = reminders

    def toDictionary(self):
        try:
            event = {
                'summary': self.summary,
                'start': self.start.toDictionary(),
                'end': self.end.toDictionary(),
                'reminders': {
                    'overrides': []
                }
            }

            event['reminders']['useDefault'] = len(self.reminders) < 1
            for reminder in self.reminders:
                event['reminders']['overrides'].append(reminder.toDictionary())
        except Exception as error:
            raise Exception("event model has invalid field value: " + str(error))
        return event


class EventDate:
    def __init__(self, dateTime, timeZone):
        self.dateTime = dateTime
        self.timeZone = timeZone

    def toDictionary(self):
        return {
            'dateTime': self.dateTime,
            'timeZone': self.timeZone,
        }


class EventReminder:
    def __init__(self, method, minutes):
        self.method = method
        self.minutes = minutes

    def toDictionary(self):
        return {
            'method': self.method,
            'minutes': self.minutes,
        }
