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
from flask_api import status
from flask_restful import Api, Resource
from marshmallow import fields
from webargs.flaskparser import use_args

from website.jsons.base import PostJson, PostPageJson, LikeJson
from website.models import Post, db, Like

api = Api(prefix='/api/posts')

put_post_args = {
    'description': fields.Str(required=False, missing=None, default=None),
    'blocked': fields.Boolean(required=False, missing=False, default=False)
}

post_posts_args = {
    'description': fields.Str(required=False, missing=None, default=None),
    'user_id': fields.Int(required=True),
    'type': fields.Str(required=True, validate=lambda t: t == 'image' or t == 'video'),
    'attachment_id': fields.Int(required=True)
}

get_posts_args = {
    'user_id': fields.Int(missing=None, required=False),
    'page': fields.Int(missing=1, required=False),
    'size': fields.Int(missing=10, required=False)
}

like_args = {
    'user_id': fields.Int(required=True)
}


class PostRoutes(Resource):

    def get(self, post_id):
        post = Post.query.filter_by(id=post_id).first()
        return PostJson(post).to_json()

    @use_args(put_post_args, locations=['json'])
    def put(self, args, post_id):
        post = Post.query.filter_by(id=post_id).first()
        post.description = args['description']
        post.blocked = args['blocked']
        db.session.commit()
        db.session.flush()
        return PostJson(post).to_json(), status.HTTP_202_ACCEPTED

    def delete(self, post_id):
        post = Post.query.filter_by(id=post_id).first()
        db.session.delete(post)
        db.session.commit()
        return '', status.HTTP_204_NO_CONTENT


class PostListRoutes(Resource):

    @use_args(post_posts_args, locations=['json'])
    def post(self, args):
        post = Post()
        post.parse(args)
        db.session.add(post)
        db.session.commit()
        return PostJson(post).to_json(), status.HTTP_201_CREATED

    @use_args(get_posts_args)
    def get(self, args):
        user_id = args['user_id']
        page = args['page']
        size = args['size']
        if user_id:
            query = Post.query.filter_by(user_id=user_id).order_by(Post.updated_at) \
                .paginate(page, error_out=True, max_per_page=size)
            return PostPageJson(query.items, page, query.pages, user_id).to_json()
        query = Post.query.order_by(Post.updated_at) \
            .paginate(page, error_out=True, max_per_page=size)
        return PostPageJson(query.items, page, query.pages).to_json()


class LikeRoutes(Resource):

    @use_args(like_args, locations=['json'])
    def post(self, args, post_id):
        like = Like(post_id, args['user_id'])
        db.session.add(like)
        db.session.commit()
        return LikeJson(like).to_json(), status.HTTP_201_CREATED

    @use_args(like_args, locations=['json'])
    def delete(self, args, post_id):
        like = Like.query.filter_by(post_id=post_id, user_id=args['user_id']).first()
        db.session.delete(like)
        db.session.commit()
        return '', status.HTTP_204_NO_CONTENT

    @use_args(like_args)
    def get(self, args, post_id):
        like = Like.query.filter_by(post_id=post_id, user_id=args['user_id']).first()
        return LikeJson(like).to_json()


def init_app(app):
    api.add_resource(LikeRoutes, '/<int:post_id>/likes/')
    api.add_resource(PostRoutes, '/<int:post_id>')
    api.add_resource(PostListRoutes, '/')
    api.init_app(app)
