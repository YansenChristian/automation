from flask import Blueprint
from flask_restful import Api
import os

ApiUrl = os.getenv("API_PREFIX") + "/health-check"
HealthCheckBlueprint = Blueprint('user', __name__, url_prefix=ApiUrl)
HealthCheckApiBlueprint = Api(HealthCheckBlueprint)


from controllers.health_check import Check
HealthCheckApiBlueprint.add_resource(Check, "")
