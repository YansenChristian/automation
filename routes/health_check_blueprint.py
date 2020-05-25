from flask import Blueprint
from flask_restful import Api
import os

ApiUrl = os.getenv("API_PREFIX") + "/health-check"
HealthCheckBlueprint = Blueprint('user', __name__, url_prefix=ApiUrl)
HealthCheckApiBlueprint = Api(HealthCheckBlueprint)


import controllers.health_check as HealthCheckController
HealthCheckApiBlueprint.add_resource(HealthCheckController.Check, "")
