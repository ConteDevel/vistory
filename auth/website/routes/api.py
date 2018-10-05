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
from flask import current_app as cur_app
from flask_api import status
from flask_restful import Resource, Api
from marshmallow import fields
from sqlalchemy import desc, or_
from webargs.flaskparser import use_args

from website.jsons.base import UserJson, UserPageJson, ChannelJson, ChannelPageJson
from website.jsons.errors import MethodNotAllowedJson
from website.models import User, Channel, db
from website.oauth2 import require_oauth

api = Api(prefix='/api')


get_args = {
    'page': fields.Int(required=False, missing=1, default=1),
    'size': fields.Int(required=False, missing=10, default=10),
    'search': fields.Str(required=False, missing=None, default=None)
}

channel_args = {
    'name': fields.Str(required=True),
    'description': fields.Str(required=False, missing=None, default=None)
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


class ChannelRoutes(Resource):

    def get(self, channel_id):
        channel = Channel.query.filter_by(id=channel_id).first()
        return ChannelJson(channel).to_json()

    @require_oauth()
    @use_args(channel_args, locations=['json'])
    def put(self, args, channel_id):
        channel = Channel.query.filter_by(id=channel_id).first()
        user = current_token.user
        if channel.user_id != user.id and user.role.name != cur_app.config['ROLE_ADMIN']:
            return MethodNotAllowedJson('').to_json(), status.HTTP_405_METHOD_NOT_ALLOWED
        channel.name = args['name']
        channel.description = args['description']
        db.session.commit()
        db.session.flush()
        return ChannelJson(channel).to_json(), status.HTTP_202_ACCEPTED

    @require_oauth()
    def delete(self, channel_id):
        channel = Channel.query.filter_by(id=channel_id).first()
        user = current_token.user
        if channel.user_id != user.id and user.role.name != cur_app.config['ROLE_ADMIN']:
            return MethodNotAllowedJson('').to_json(), status.HTTP_405_METHOD_NOT_ALLOWED
        db.session.delete(channel)
        db.session.commit()
        return '', status.HTTP_204_NO_CONTENT


class UserListRoutes(Resource):

    @use_args(get_args)
    def get(self, args):
        page = args['page']
        size = args['size']
        search = '%' + args['search'] + '%'
        query = User.query
        if search:
            query = query.filter(or_(
                User.first_name.ilike(search),
                User.last_name.ilike(search),
                User.email.ilike(search),
            ))
        query = query.order_by(User.first_name, User.last_name)\
            .paginate(page, max_per_page=size, error_out=True)
        return UserPageJson(query.items, page, query.pages).to_json()


class ChannelListRoutes(Resource):

    @require_oauth
    @use_args(channel_args, locations=['json'])
    def post(self, args):
        channel = Channel()
        channel.name = args['name']
        channel.description = args['description']
        channel.user_id = current_token.user.id
        db.session.commit()
        db.session.flush()
        return ChannelJson(channel).to_json(), status.HTTP_202_ACCEPTED

    @use_args(get_args)
    def get(self, args):
        page = args['page']
        size = args['size']
        search = '%' + args['search'] + '%'
        query = Channel.query
        if search:
            query = query.filter(Channel.name.ilike(search))
        query = query.order_by(Channel.name, desc(Channel.created_at))\
            .paginate(page, max_per_page=size, error_out=True)
        return ChannelPageJson(query.items, page, query.pages).to_json()


def init_app(app):
    api.add_resource(UserListRoutes, '/users')
    api.add_resource(MeRoutes, '/users/me')
    api.add_resource(UserRoutes, '/users/<int:user_id>')
    api.add_resource(ChannelListRoutes, '/channels')
    api.add_resource(ChannelRoutes, '/channels/<int:channel_id>')
    api.init_app(app)
