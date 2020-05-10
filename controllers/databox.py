import services.databox as DataboxService
import utilities.http_response as response
from utilities.databox_client import getDataboxClient
from flask_restful import Resource
from models.databox import Metric


class SyncMetric(Resource):
    def post(self):
        data = []
        data.append(DataboxService.syncProductivityWithGoalify())
        data.append(DataboxService.syncDisciplineWithGoalify())
        data.append(DataboxService.syncCommitmentWithAsana())

        totalTimeManagementScore = sum([metric['value'] for metric in data])
        timeManagementAverageScore = totalTimeManagementScore / len(data)
        data.append(Metric("Time Management Summary", timeManagementAverageScore, "%").toDictionary())

        databoxClient = getDataboxClient()
        result = databoxClient.insert_all(data)
        return response.returnData(200, result)
