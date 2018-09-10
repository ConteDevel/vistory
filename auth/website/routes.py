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
from flask import request, render_template, Blueprint, session, redirect, jsonify, url_for
from flask_api import status
from flask_wtf import CSRFProtect

from website.forms import SignUpForm
from website.models import User, db
from website.oauth2 import server, current_user, require_oauth

bp = Blueprint(__name__, 'home')
csrf = CSRFProtect()


@bp.route('/')
def home():
    user = current_user()
    if not user:
        return redirect(url_for('website.routes.sign_in'), status.HTTP_302_FOUND)
    return redirect('vistory.com')


@bp.route('/signin', methods=('GET', 'POST'))
def sign_in():
    if request.method == 'POST':
        username = request.form.get('username')
        user = User.query.filter_by(username=username).first()
        if not user:
            user = User(username=username)
            db.session.add(user)
            db.session.commit()
        session['id'] = user.id
        return redirect('/')
    user = current_user()
    return render_template('sign_in.html', user=user, clients=[])


@bp.route('/signup', methods=('GET', 'POST'))
def sign_up():
    form = SignUpForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(email=form.email.data).first()
        if not user:
            user = form.to_user()
            db.session.add(user)
            return redirect(url_for('website.routes.sign_in'), status.HTTP_302_FOUND)
    return render_template('sign_up.html', form=form)


@bp.route("/oauth/authorize", methods=['GET', 'POST'])
def authorize():
    user = current_user()
    if request.method == 'GET':
        grant = server.validate_consent_request(end_user=user)
        return render_template(
            "authorize.html",
            grant=grant,
            user=user
        )
    confirmed = request.form['confirm']
    if confirmed:
        # granted by resource owner
        return server.create_authorization_response(user)
    # denied by resource owner
    return server.create_authorization_response(None)


@bp.route('/oauth/token', methods=['POST'])
def issue_token():
    return server.create_token_response()


@bp.route('/oauth/revoke', methods=['POST'])
def revoke_token():
    return server.create_endpoint_response('revocation')


@bp.route('/api/me')
@require_oauth('profile')
def api_me():
    user = current_token.user
    return jsonify(id=user.id, username=user.username)


def init_routes(app):
    app.register_blueprint(bp, urlprefix='')
    csrf.init_app(app)
