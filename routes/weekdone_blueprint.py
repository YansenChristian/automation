from flask import Blueprint
from flask_restful import Api
import os

ApiUrl = os.getenv("API_PREFIX") + "/weekdone"
WeekdoneBlueprint = Blueprint('weekdone', __name__, url_prefix=ApiUrl)
WeekdoneApiBlueprint = Api(WeekdoneBlueprint)


from controllers.weekdone import SyncKeyResults
WeekdoneApiBlueprint.add_resource(SyncKeyResults, "/sync")