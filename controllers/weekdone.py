import services.weekdone as weekdoneService
import utilities.http_response as response
from flask_restful import Resource


class SyncKeyResults(Resource):
    def post(self):
        data = weekdoneService.syncProductivityWithGoalify()
        return response.returnData(200, data), 200