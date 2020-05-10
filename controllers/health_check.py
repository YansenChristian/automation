import utilities.http_response as response
from flask_restful import Resource


class Check(Resource):
    def get(self):
        return response.returnMessage(200, "OK")
