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
from authlib.common.security import generate_token
from authlib.flask.oauth2 import AuthorizationServer, ResourceProtector
from authlib.specs.rfc6749 import grants
from flask import session

from website.models import Client, Token, db, User, AuthorizationCode

server = AuthorizationServer()
require_oauth = ResourceProtector()


class AuthorizationCodeGrant(grants.AuthorizationCodeGrant):
    def create_authorization_code(self, client, grant_user, request):
        # you can use other method to generate this code
        code = generate_token(48)
        item = AuthorizationCode(
            code=code,
            client_id=client.client_id,
            redirect_uri=request.redirect_uri,
            scope=request.scope,
            user_id=grant_user.get_user_id(),
        )
        db.session.add(item)
        db.session.commit()
        return code

    def parse_authorization_code(self, code, client):
        item = AuthorizationCode.query.filter_by(code=code, client_id=client.client_id)\
            .first()
        if item and not item.is_expired():
            return item

    def delete_authorization_code(self, authorization_code):
        db.session.delete(authorization_code)
        db.session.commit()

    def authenticate_user(self, authorization_code):
        return User.query.get(authorization_code.user_id)


def current_user():
    if 'id' in session:
        uid = session['id']
        return User.query.get(uid)
    return None


def query_client(client_id):
    return Client.query.filter_by(client_id=client_id).first


def save_token(token, request):
    if request.user:
        user_id = request.user.get_user_id()
    else:
        # client_credentials grant_type
        user_id = request.client.user_id
    item = Token(
        client_id=request.client.client_id,
        user_id=user_id,
        **token
    )
    db.session.add(item)
    db.session.commit()


def init_oauth2(app):
    server.init_app(app, query_client=query_client, save_token=save_token)
    # register it to grant endpoint
    server.register_grant(AuthorizationCodeGrant)
