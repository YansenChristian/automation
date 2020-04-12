import utilities.http_response as response
import constants.asana
from utilities.asana_client import getAsanaClient
from flask_restful import Resource


class MoveTodayRoutinityTaskToOverview(Resource):
    def post(self):
        asanaClient = getAsanaClient()
        routinityProjectId = constants.asana.PROJECTS['Routinity']['gid']
        overviewProjectId = constants.asana.PROJECTS['Overview']['gid']
        inProgressSectionId = constants.asana.PROJECTS['Overview']['sections']['In Progress']['gid']
        data = asanaClient.moveTodayTasksAcrossProjects(routinityProjectId, overviewProjectId, inProgressSectionId)
        return response.returnData(200, data)