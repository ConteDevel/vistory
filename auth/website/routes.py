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

from flask import request, render_template, Blueprint, session, redirect, url_for
from flask_restful import Resource, Api, reqparse
from werkzeug.security import gen_salt

from website.forms import SignUpForm, SignInForm, ClientForm
from website.jsons import UserJson, ErrorJson, UsersJson
from website.models import User, db, Client
from website.oauth2 import server, current_user, GRANT_TYPES, RESPONSE_TYPES

api = Api(prefix='/api')
bp = Blueprint('bp', __name__)
logger = None


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user():
            return redirect(url_for('bp.sign_in', next=request.url))
        return f(*args, **kwargs)
    return decorated_function


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = current_user()
        if not (user and user.admin):
            return redirect(url_for('bp.sign_in', next=request.url))
        return f(*args, **kwargs)
    return decorated_function


@bp.route('/')
@login_required
def home():
    logger.debug('home')
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
        client.grant_types = GRANT_TYPES
        client.response_type = RESPONSE_TYPES
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


@bp.route("/oauth/authorize", methods=['GET'])
@login_required
def authorize():
    user = current_user()
    return server.create_authorization_response(grant_user=user)


@bp.route('/oauth/token', methods=['POST'])
def issue_token():
    return server.create_token_response()


@bp.route('/oauth/verify', methods=['POST'])
def verify_token():
    pass


@bp.route('/oauth/revoke', methods=['POST'])
def revoke_token():
    return server.create_endpoint_response('revocation')


class UserRoutes(Resource):

    def get(self, user_id):
        user = User.query.filter_by(id=user_id).first()
        if user:
            return UserJson(user).to_json()
        return ErrorJson(404, 'NOT_FOUND', 'User not found.'), 404


class UserListRoutes(Resource):

    def __init__(self):
        self.parser = reqparse.RequestParser(bundle_errors=True)
        self.parser.add_argument('page', type=int, required=False)
        self.parser.add_argument('size', type=int, required=False)

    def get(self):
        args = self.parser.parse_args()
        page = args['page'] if args['page'] else 0
        size = args['size'] if args['size'] else 10
        query = User.query.order_by(User.first_name, User.last_name)\
            .paginate(page, size, error_out=False)
        return UsersJson(query.items, page, query.pages).to_json()


def init_routes(app):
    global logger
    logger = app.logger
    # Initialize routes
    app.register_blueprint(bp, urlprefix='')
    api.add_resource(UserListRoutes, '/users')
    api.add_resource(UserRoutes, '/users/<user_id>')
    api.init_app(app)
