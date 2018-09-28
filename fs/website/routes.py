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
from os import path

import werkzeug
from flask import Blueprint, make_response, url_for
from flask_restful import Api, Resource, reqparse
from werkzeug.utils import secure_filename

from website.jsons import ErrorJson, ImageJson, VideoJson
from website.models import Image, db, Video

api = Api()
bp = Blueprint('bp', __name__)
logger = None
img_exts = None
video_exts = None


def is_allowed_img(file):
    if file:
        _, ext = path.splitext(secure_filename(file.filename))
        return ext.lower() in img_exts
    return False


def is_allowed_video(file):
    if file:
        _, ext = path.splitext(secure_filename(file.filename))
        return ext.lower() in video_exts
    return False


@bp.route('/images/<img_id>/file')
def download_img(img_id):
    image = Image.query.filter_by(id=img_id).first()
    if image is not None:
        response = make_response(image.file)
        response.headers['Content-Type'] = image.mime
        response.headers['Content-Dispostion'] = "attachment; filename={0}{1}"\
            .format(img_id, image.extension)
        return response
    return ErrorJson(404, 'NOT_FOUND', 'Image not found.').to_json(), 404


@bp.route('/videos/<video_id>/file')
def download_video(video_id):
    video = Video.query.filter_by(id=video_id).first()
    if video is not None:
        response = make_response(video.file)
        response.headers['Content-Type'] = video.mime
        response.headers['Content-Dispostion'] = "attachment; filename={0}{1}"\
            .format(video_id, video.extension)
        return response
    return ErrorJson(404, 'NOT_FOUND', 'Video not found.').to_json(), 404


class ImageRoutes(Resource):

    def get(self, img_id):
        image = Image.query.filter_by(id=img_id).first()
        url = url_for('bp.download_img', img_id=img_id, _external=True)
        if image is not None:
            return ImageJson(image, url).to_json()
        return ErrorJson(404, 'NOT_FOUND', 'Image not found.').to_json(), 404


class VideoRoutes(Resource):

    def get(self, video_id):
        video = Video.query.filter_by(id=video_id).first()
        url = url_for('bp.download_video', video_id=video_id, _external=True)
        if video is not None:
            return VideoJson(video, url).to_json()
        return ErrorJson(404, 'NOT_FOUND', 'Video not found.').to_json(), 404


class ImageListRoutes(Resource):

    def post(self):
        parse = reqparse.RequestParser()
        parse.add_argument('image', type=werkzeug.FileStorage, location='files')
        args = parse.parse_args()
        file = args['image']
        if is_allowed_img(file):
            image = Image(file)
            db.session.add(image)
            db.session.commit()

            return ImageJson(image, '/').to_json(), 201
        return ErrorJson(400, 'BAD_REQUEST', 'Image format is not supported.').to_json(), 400


class VideoListRoutes(Resource):

    def post(self):
        parse = reqparse.RequestParser()
        parse.add_argument('video', type=werkzeug.FileStorage, location='files')
        args = parse.parse_args()
        file = args['video']
        if is_allowed_video(file):
            video = Video(file)
            db.session.add(video)
            db.session.commit()

            return VideoJson(video, '/').to_json(), 201
        return ErrorJson(400, 'BAD_REQUEST', 'Video format is not supported.').to_json(), 400


def init_routes(app):
    global logger, img_exts, video_exts
    logger = app.logger
    img_exts = app.config['IMG_ALLOWED_EXTENSIONS']
    video_exts = app.config['VIDEO_ALLOWED_EXTENSIONS']
    # Initialize routing
    app.register_blueprint(bp)
    # Initialize RESTful API
    api.add_resource(ImageRoutes, '/images/<img_id>')
    api.add_resource(VideoRoutes, '/videos/<video_id>')
    api.add_resource(ImageListRoutes, '/images')
    api.add_resource(VideoListRoutes, '/videos')
    api.init_app(app)
