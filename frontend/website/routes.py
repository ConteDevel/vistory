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
import ssl
import urllib
from functools import wraps
from urllib import parse

from flask import render_template, Blueprint, request, redirect, url_for
from flask_restful import Api

api = Api()
bp = Blueprint('bp', __name__)
logger = None
config = None


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'Authorization' not in request.headers:
            home_url = url_for('bp.home')
            return redirect(url_for(config['AUTH_SERVICE'], next=home_url, _external=True))
        return f(*args, **kwargs)
    return decorated_function


@bp.route('/')
@login_required
def home():
    return render_template("home.html")


@bp.route('/callback/<code>')
def callback(code):
    url = '{0}/oauth/token'.format(config['AUTH_SERVICE'])
    data = parse.urlencode({
        'client_id': config['CLIENT_ID'],
        'client_secret': config['CLIENT_SECRET'],
        'grant_type': 'authorization_code',
        'code': code
    }).encode()
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    r = urllib.request.urlopen(url, data, context=ctx)
    return print(r.read())


def init_routes(app):
    global logger, config
    logger = app.logger
    config = app.config
    # Initialize routes
    app.register_blueprint(bp, urlprefix='')
    # Add your RESTful routes below
    api.init_app(app)
