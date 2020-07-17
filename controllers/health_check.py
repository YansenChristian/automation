import utilities.http_response as response
from flask_restful import Resource
from utilities.logger import getLogger


class Check(Resource):
    def get(self):
        logger = getLogger()
        logger.error("no way")
        return response.returnMessage(200, "OK")
