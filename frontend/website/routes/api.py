from flask import current_app as app
from flask_restful import Resource
from marshmallow import fields
from webargs.flaskparser import use_args

from website import sender

bearer_args = {
    'Authorization': fields.Str(required=True, validate=lambda b: b.startswith('Bearer '))
}


class MeRoutes(Resource):

    @use_args(bearer_args, locations=['headers'])
    def get(self, args):
        url = app.config['AUTH_SERVICE'] + '/api/users/me'
        return sender.get(url, args['Authorization'])
