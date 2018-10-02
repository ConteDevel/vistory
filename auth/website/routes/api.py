"""
    This file is part of Vistory.

    Vistory is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Vistory is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Vistory.  If not, see <http://www.gnu.org/licenses/>.
"""
from authlib.flask.oauth2 import current_token
from flask_restful import Resource, Api
from marshmallow import fields
from webargs.flaskparser import use_args

from website.jsons.base import UserJson, UserPageJson
from website.models import User
from website.oauth2 import require_oauth

api = Api(prefix='/api')


get_users_args = {
    'page': fields.Int(required=False, missing=1, default=1),
    'size': fields.Int(required=False, missing=10, default=10)
}


class MeRoutes(Resource):

    @require_oauth()
    def get(self):
        user = current_token.user
        return UserJson(user).to_json()


class UserRoutes(Resource):

    def get(self, user_id):
        user = User.query.filter_by(id=user_id).first()
        return UserJson(user).to_json()


class UserListRoutes(Resource):

    @use_args(get_users_args)
    def get(self, args):
        page = args['page']
        size = args['size']
        query = User.query.order_by(User.first_name, User.last_name)\
            .paginate(page, size, error_out=False)
        return UserPageJson(query.items, page, query.pages).to_json()


def init_app(app):
    api.add_resource(UserListRoutes, '/users')
    api.add_resource(MeRoutes, '/users/me')
    api.add_resource(UserRoutes, '/users/<int:user_id>')
    api.init_app(app)
