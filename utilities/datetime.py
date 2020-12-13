import datetime
import pytz


def getTodayDateInStringFormat(dateTimeFormat):
	nowDateTime = datetime.datetime.now(
		pytz.timezone('Asia/Jakarta')
	)
	return nowDateTime.strftime(dateTimeFormat)


def validateStringFormat(dateTimeText, dateTimeFormat):
	try:
		datetime.datetime.strptime(dateTimeText, dateTimeFormat)
	except ValueError:
		raise ValueError("Incorrect data format, should be " + dateTimeFormat)
