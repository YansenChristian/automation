from flask import Blueprint
from flask_restful import Api
import os

ApiUrl = os.getenv("API_PREFIX") + "/instagantt"
InstaganttBlueprint = Blueprint('instagantt', __name__, url_prefix=ApiUrl)
InstaganttApiBlueprint = Api(InstaganttBlueprint)


from controllers.instagantt import GetAllTasks
InstaganttApiBlueprint.add_resource(GetAllTasks, "/tasks")
