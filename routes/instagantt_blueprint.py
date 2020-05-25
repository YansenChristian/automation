from flask import Blueprint
from flask_restful import Api
import os

ApiUrl = os.getenv("API_PREFIX") + "/instagantt"
InstaganttBlueprint = Blueprint('instagantt', __name__, url_prefix=ApiUrl)
InstaganttApiBlueprint = Api(InstaganttBlueprint)


import controllers.instagantt as InstaganttController
InstaganttApiBlueprint.add_resource(InstaganttController.GetAllTasks, "/tasks")
