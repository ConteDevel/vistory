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
from flask import Blueprint, current_app as app, request, redirect, url_for, render_template

from website import sender
from website.sender import to_basic

bp = Blueprint('oauth2', __name__)


@bp.route('/callback')
def callback():
    code = request.args.get('code')
    state = request.args.get('state')
    if state != app.config['SECRET_KEY']:
        return redirect(url_for('bp.home'))
    url = '{0}/oauth/token'.format(app.config['AUTH_SERVICE'])
    fields = {
        'client_id': app.config['CLIENT_ID'],
        'client_secret': app.config['CLIENT_SECRET'],
        'grant_type': 'authorization_code',
        'code': code,
        'state': state
    }
    auth = to_basic(app.config['CLIENT_ID'], app.config['CLIENT_SECRET'])
    token, _ = sender.post(url, fields=fields, auth=auth)
    return render_template("callback.html", token=token)
