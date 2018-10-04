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

import requests
from flask import render_template, Blueprint, current_app as cur_app, request

from website.forms import NewPostForm
from website.jsons.errors import ErrorJson, UnprocessableEntityJson

bp = Blueprint('bp', __name__)
PAGES = [
    'new_channel.vue',
    'search_results.vue',
    'profile.vue',
    'posts.vue',
    'people.vue',
    'channels.vue'
]
IMG_ALLOWED_EXTENSIONS = {'.png', '.jpg', '.jpeg'}
VIDEO_ALLOWED_EXTENSIONS = {'.mp4'}


def get_file_type(file):
    extension = path.splitext(file.filename)[1].lower()
    if extension in IMG_ALLOWED_EXTENSIONS:
        return 'image'
    if extension in VIDEO_ALLOWED_EXTENSIONS:
        return 'video'
    raise UnprocessableEntityJson('Unsupported file type.')


@bp.route('/')
def home():
    sign_in_url = '{0}/oauth/authorize?client_id={1}&response_type=code&state={2}'\
        .format(cur_app.config['AUTH_SERVICE'], cur_app.config['CLIENT_ID'], cur_app.config['SECRET_KEY'])
    return render_template("home.html", sign_in_url=sign_in_url)


@bp.route('/pages/new_post.vue', methods=['GET', 'POST'])
def new_post():
    form = NewPostForm(request.form)
    form.file.data = request.files.get('file', '')
    if request.method == 'POST' and form.validate():
        file = form.file.data
        f_type = get_file_type(file)
        files = {f_type: file.read()}
        fs_url = cur_app.config['FS_SERVICE'] + '/api/' + f_type + 's'
        response = requests.post(fs_url, files=files)

    return render_template('pages/new_post.vue', form=form)


@bp.route('/pages/<page_name>')
def get_page(page_name):
    if page_name not in PAGES:
        return ErrorJson(404, 'NOT_FOUND', 'Requested page not found.').to_json(), 404
    return render_template('pages/%s' % page_name)
