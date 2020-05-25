import services.databox_productivity_metrics_sync.service as ProductivityMetricsSyncService
import utilities.http_response as response
from flask_restful import Resource


class SyncProductivityMetrics(Resource):
    def post(self):
        result = ProductivityMetricsSyncService.Run()
        return response.returnData(200, result)
