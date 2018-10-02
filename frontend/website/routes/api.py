from flask_restful import Resource

from website.routes.base import oauth2_required


class MeRoutes(Resource):

    @oauth2_required
    def get(self):
        pass