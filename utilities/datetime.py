import datetime


def getTodayDateInFormat(dateTimeFormat):
	nowDateTime = datetime.datetime.now()
	nowDateTime += datetime.timedelta(hours=7)
	return nowDateTime.strftime(dateTimeFormat)


def validateStringFormat(dateTimeText, dateTimeFormat):
	try:
		datetime.datetime.strptime(dateTimeText, dateTimeFormat)
	except ValueError:
		raise ValueError("Incorrect data format, should be " + dateTimeFormat)
