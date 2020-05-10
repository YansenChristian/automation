import datetime


def getTodayDateInFormat(format):
	nowDateTime = datetime.datetime.now()
	nowDateTime += datetime.timedelta(hours=7)
	return nowDateTime.strftime(format)
