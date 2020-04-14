import services.weekdone as weekdoneService
import utilities.http_response as response
from flask_restful import Resource


class SyncKeyResults(Resource):
    def post(self):
        data = []
        data.append(weekdoneService.syncProductivityWithGoalify())
        data.append(weekdoneService.syncDisciplineWithGoalify())
        data.append(weekdoneService.syncCommitmentWithGoalify())
        return response.returnData(200, data)
