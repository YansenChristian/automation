from flask import Blueprint
from flask_restful import Api
import os

ApiUrl = os.getenv("API_PREFIX") + "/asana"
AsanaBlueprint = Blueprint('asana', __name__, url_prefix=ApiUrl)
AsanaApiBlueprint = Api(AsanaBlueprint)


import controllers.asana as AsanaController
AsanaApiBlueprint.add_resource(AsanaController.MoveTodayRoutinityTasksToOverview, "/move-routinity-to-overview")
