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
from functools import wraps

from authlib.flask.oauth2 import current_token
from flask import request, render_template, Blueprint, session, redirect, jsonify, url_for
from werkzeug.security import gen_salt

from website.forms import SignUpForm, SignInForm, ClientForm
from website.models import User, db, Client
from website.oauth2 import server, current_user, require_oauth

bp = Blueprint(__name__, 'home')


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user():
            return redirect(url_for('website.routes.sign_in', next=request.url))
        return f(*args, **kwargs)
    return decorated_function


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = current_user()
        if not (user and user.admin):
            return redirect(url_for('website.routes.sign_in', next=request.url))
        return f(*args, **kwargs)
    return decorated_function


@bp.route('/')
@login_required
def home():
    user = current_user()
    if user.admin:
        clients = Client.query.filter_by(user_id=user.id).all()
        form = ClientForm(request.form)
        return render_template("home.html", user=user, clients=clients, form=form)
    return redirect('vistory.com')


@bp.route('/create_client', methods=['POST'])
@admin_required
def create_client():
    form = ClientForm(request.form)
    if form.validate():
        user = current_user()
        client = form.to_client()
        client.user_id = user.id
        client.client_id = gen_salt(24)
        client.client_secret = gen_salt(48)
        db.session.add(client)
        db.session.commit()
    return redirect('/')


@bp.route('/signin', methods=['GET', 'POST'])
def sign_in():
    form = SignInForm(request.form)
    next_url = request.args.get('next')
    if next_url:
        form.next.data = next_url
    if request.method == 'POST' and form.validate():
        email = form.email.data
        user = User.query.filter_by(email=email).first()
        if not (user and user.check_password(form.password.data)):
            render_template('sign_in.html', form=form, error_msg='Invalid email or password')
        session['id'] = user.id
        return redirect('/')
    return render_template('sign_in.html', form=form)


@bp.route('/signout')
def sign_out():
    del session['id']
    return redirect('/signin')


@bp.route('/signup', methods=['GET', 'POST'])
def sign_up():
    form = SignUpForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(email=form.email.data).first()
        if not user:
            user = form.to_user()
            db.session.add(user)
            db.session.commit()
            return redirect('/signin')
    return render_template('sign_up.html', form=form)


@bp.route("/oauth/authorize", methods=['GET', 'POST'])
@login_required
def authorize():
    user = current_user()
    return server.create_authorization_response(user)


@bp.route('/oauth/token', methods=['POST'])
def issue_token():
    return server.create_token_response()


@bp.route('/oauth/revoke', methods=['POST'])
def revoke_token():
    return server.create_endpoint_response('revocation')


@bp.route('/api/me')
@require_oauth(None)
def api_me():
    user = current_token.user
    return jsonify(id=user.id, username=user.username)


def init_routes(app):
    app.register_blueprint(bp, urlprefix='')
