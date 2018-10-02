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
import urllib.request
from base64 import b64encode
from urllib import parse

from flask import Blueprint, current_app as app, request, redirect, url_for, render_template

bp = Blueprint('oauth2', __name__)

# Create a SSL context to accept not-trusted certificates
untrusted_ssl_ctx = ssl.create_default_context()
untrusted_ssl_ctx.check_hostname = False
untrusted_ssl_ctx.verify_mode = ssl.CERT_NONE


def send_post(url, data):
    # Create a header for the basic authorization
    client_id_secret = app.config['CLIENT_ID'] + ":" + app.config['CLIENT_SECRET']
    auth = b64encode(bytes(client_id_secret, 'ascii')).decode('ascii')
    basic_header = {'Authorization': 'Basic ' + auth}
    # Prepare a request
    req = urllib.request.Request(url, data, basic_header, unverifiable=True)
    response = urllib.request.urlopen(req, context=untrusted_ssl_ctx)
    json = response.read().decode('utf-8')
    return json


@bp.route('/callback')
def callback():
    code = request.args.get('code')
    state = request.args.get('state')
    if state != app.config['SECRET_KEY']:
        return redirect(url_for('bp.home'))
    url = '{0}/oauth/token'.format(app.config['AUTH_SERVICE'])
    data = parse.urlencode({
        'client_id': app.config['CLIENT_ID'],
        'client_secret': app.config['CLIENT_SECRET'],
        'grant_type': 'authorization_code',
        'code': code,
        'state': state
    }).encode()
    token = send_post(url, data)
    return render_template("callback.html", token=token)
