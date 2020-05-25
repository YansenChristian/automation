from flask import Blueprint
from flask_restful import Api
import os

ApiUrl = os.getenv("API_PREFIX") + "/databox"
DataboxBlueprint = Blueprint('databox', __name__, url_prefix=ApiUrl)
DataboxApiBlueprint = Api(DataboxBlueprint)


import controllers.databox as DataboxController
DataboxApiBlueprint.add_resource(DataboxController.SyncProductivityMetrics, "/productivity/sync")
