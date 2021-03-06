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
from authlib.flask.oauth2.sqla import create_revocation_endpoint, create_bearer_token_validator
from authlib.specs.rfc6749 import grants
from flask import session

from website.models import Client, Token, db, User, AuthorizationCode

GRANT_TYPES = [
    'authorization_code',
    'refresh_token'
]

RESPONSE_TYPES = [
    'code'
]

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


class PasswordGrant(grants.ResourceOwnerPasswordCredentialsGrant):
    def authenticate_user(self, email, password):
        user = User.query.filter_by(email=email).first()
        if user.check_password(password):
            return user


class RefreshTokenGrant(grants.RefreshTokenGrant):
    def authenticate_refresh_token(self, refresh_token):
        item = Token.query.filter_by(refresh_token=refresh_token).first()
        if item and not item.is_refresh_token_expired():
            return item

    def authenticate_user(self, credential):
        return User.query.get(credential.user_id)


def current_user():
    if 'id' in session:
        uid = session['id']
        return User.query.get(uid)
    return None


def query_client(client_id):
    return Client.query.filter_by(client_id=client_id).first()


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


server = AuthorizationServer(query_client=query_client, save_token=save_token)


def init_app(app):
    server.init_app(app)
    # register it to grant endpoint
    server.register_grant(grants.ImplicitGrant)
    server.register_grant(AuthorizationCodeGrant)
    server.register_grant(grants.ClientCredentialsGrant)
    server.register_grant(PasswordGrant)
    server.register_grant(RefreshTokenGrant)
    # support revocation
    revocation_cls = create_revocation_endpoint(db.session, Token)
    server.register_endpoint(revocation_cls)
    # protect resource
    bearer_cls = create_bearer_token_validator(db.session, Token)
    require_oauth.register_token_validator(bearer_cls())
