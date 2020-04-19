import utilities.datetime as DatetimeHelper


class Metric:
	def __init__(self, key, value, unit, category = None, date = None):
		self.key = key
		self.value = value
		self.unit = unit
		self.date = date if date is not None else DatetimeHelper.getTodayDateInFormat("%Y-%m-%d")
		self.category = category

	def toDictionary(self):
		metric = {}
		metric['key'] = self.key
		metric['value'] = self.value
		metric['unit'] = self.unit
		metric['date'] = self.date
		if self.category is not None:
			metric['attributes'] = { 'category': self.category }
		return metric