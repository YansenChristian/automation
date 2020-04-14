import utilities.http_response as response
from utilities.zapier_storage_client import getZapierStorageClient
from flask_restful import Resource


class Check(Resource):
    def get(self):
        return response.returnMessage(200, "OK")