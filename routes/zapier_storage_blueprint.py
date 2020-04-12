from flask import Blueprint
from flask_restful import Api
import os

ApiUrl = os.getenv("API_PREFIX") + "/zapier-storage"
ZapierStorageBlueprint = Blueprint('zapier-storage', __name__, url_prefix=ApiUrl)
ZapierStorageApiBlueprint = Api(ZapierStorageBlueprint)


import controllers.zapier_storage as ZapierStorageController
ZapierStorageApiBlueprint.add_resource(ZapierStorageController.IncreaseTodayTasksCounterByOne, "/increase-today-tasks")
ZapierStorageApiBlueprint.add_resource(ZapierStorageController.IncreaseTodayCompletedTasksCounterByOne, "/increase-today-completed-tasks")