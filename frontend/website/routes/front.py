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
from flask import render_template, Blueprint, current_app as cur_app

from website.jsons.errors import ErrorJson

bp = Blueprint('bp', __name__)
PAGES = [
    'new_post',
    'new_channel',
    'search_results',
    'profile',
    'posts',
    'people',
    'channels'
]


@bp.route('/')
def home():
    sign_in_url = '{0}/oauth/authorize?client_id={1}&response_type=code&state={2}'\
        .format(cur_app.config['AUTH_SERVICE'], cur_app.config['CLIENT_ID'], cur_app.config['SECRET_KEY'])
    return render_template("home.html", sign_in_url=sign_in_url)


@bp.route('/pages/<page_name>')
def get_page(page_name):
    if page_name not in PAGES:
        return ErrorJson(404, 'NOT_FOUND', 'Requested page not found.').to_json(), 404
    return render_template('pages/%s.html' % page_name)
