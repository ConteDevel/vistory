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
from flask import request
from flask_restful import Api, Resource

from website.jsons import PostJson, ChannelPostJson
from website.models import Post, db

api = Api(prefix='/api/posts')
logger = None


class PostRoutes(Resource):
    def get(self, post_id):
        post = Post.query.filter_by(id=post_id).first()
        return ChannelPostJson(post).to_json()


class PostListRoutes(Resource):
    def post(self):
        json_data = request.get_json(force=True)
        post = Post()
        post.parse(json_data)
        db.session.add(post)
        db.session.commit()
        return PostJson(post).to_json()

    def get(self):
        pass


def init_app(app):
    global logger
    logger = app.logger
    api.add_resource(PostRoutes, '/<post_id>')
    api.add_resource(PostListRoutes, '/')
    api.init_app(app)
