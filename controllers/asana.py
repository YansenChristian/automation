import utilities.http_response as response
import constants.asana
import services.asana as AsanaService
from flask_restful import Resource


class MoveTodayRoutinityTasksToOverview(Resource):
    def post(self):
        routinityProjectId = constants.asana.PROJECTS['Routinity']['gid']
        overviewProjectId = constants.asana.PROJECTS['Overview']['gid']
        inProgressSectionId = constants.asana.PROJECTS['Overview']['sections']['In Progress']['gid']
        data = AsanaService.moveTodayTasksAcrossProjects(routinityProjectId, overviewProjectId, inProgressSectionId)
        return response.returnData(200, data)
