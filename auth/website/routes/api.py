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
from flask_restful import Resource, reqparse, Api

from website.jsons import UserJson, UsersJson
from website.models import User


api = Api(prefix='/api')


class UserRoutes(Resource):

    def get(self, user_id):
        user = User.query.filter_by(id=user_id).first()
        if user:
            return UserJson(user).to_json()
        return ErrorJson(404, 'NOT_FOUND', 'User not found.'), 404


class UserListRoutes(Resource):

    def __init__(self):
        self.parser = reqparse.RequestParser(bundle_errors=True)
        self.parser.add_argument('page', type=int, required=False)
        self.parser.add_argument('size', type=int, required=False)

    def get(self):
        args = self.parser.parse_args()
        page = args['page'] if args['page'] else 0
        size = args['size'] if args['size'] else 10
        query = User.query.order_by(User.first_name, User.last_name)\
            .paginate(page, size, error_out=False)
        return UsersJson(query.items, page, query.pages).to_json()


def init_app(app):
    api.add_resource(UserListRoutes, '/users')
    api.add_resource(UserRoutes, '/users/<user_id>')
    api.init_app(app)
