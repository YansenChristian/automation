import utilities.http_response as response
import services.sync_instagantt_to_gcalendar_asana.service as SyncToAsanaGCalendarService
from utilities.api_clients.instagantt_client import getInstaganttClient
from flask_restful import Resource


class GetAllTasks(Resource):
    def get(self):
        client = getInstaganttClient()
        return response.returnData(200, client.getAll())


class SyncToAsanaGCalendar(Resource):
    def post(self):
        return response.returnData(200, SyncToAsanaGCalendarService.Run())
