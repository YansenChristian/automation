from flask import Blueprint
from flask_restful import Api
import os

ApiUrl = os.getenv("API_PREFIX") + "/asana"
AsanaBlueprint = Blueprint('asana', __name__, url_prefix=ApiUrl)
AsanaApiBlueprint = Api(AsanaBlueprint)


from controllers.asana import MoveTodayRoutinityTasksToOverview
AsanaApiBlueprint.add_resource(MoveTodayRoutinityTasksToOverview, "/move-routinity-to-overview")
