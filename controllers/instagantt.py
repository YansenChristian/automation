import utilities.http_response as response
from utilities.instagantt_client import getInstaganttClient
from flask_restful import Resource


class GetAllTasks(Resource):
    def get(self):
        client = getInstaganttClient()
        return response.returnData(200, client.getAllTasks())
