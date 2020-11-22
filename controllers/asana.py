import utilities.http_response as response
import constants.asana
import services.common.asana as AsanaService
from flask_restful import Resource


class MoveTodayRoutinityTasksToInBasket(Resource):
    def post(self):
        routinityProjectId = constants.asana.PROJECTS['Routinity']['gid']
        inBasketProjectId = constants.asana.PROJECTS['In-Basket']['gid']
        inBasketStuffSectionId = constants.asana.PROJECTS['In-Basket']['sections']['Stuff']['gid']
        data = AsanaService.moveTodayTasksAcrossProjects(routinityProjectId, inBasketProjectId, inBasketStuffSectionId)
        return response.returnData(200, data)
