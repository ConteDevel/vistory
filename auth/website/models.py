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
    along with Vistory. If not, see <http://www.gnu.org/licenses/>.
"""
from datetime import datetime
import enum
import time

from authlib.flask.oauth2.sqla import OAuth2ClientMixin, OAuth2TokenMixin, OAuth2AuthorizationCodeMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import UniqueConstraint, ForeignKey
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class Gender(enum.Enum):
    Female = 0,
    Male = 1


class BaseMixin(object):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_at = db.Column('created_at', db.DateTime, default=datetime.now, nullable=False)
    updated_at = db.Column('updated_at', db.DateTime, default=datetime.now,
                           onupdate=datetime.now, nullable=False)


class Role(db.Model, BaseMixin):
    __tablename__ = 'roles'
    __table_args__ = (UniqueConstraint('name', 'uq_roles_name'))
    name = db.Column(db.String(32), nullable=False)

    users = db.relationship("User", back_populates="role")


class User(db.Model, BaseMixin):
    __tablename__ = 'users'
    email = db.Column(db.String(255), nullable=False)
    phone_number = db.Column(db.String(15), nullable=False)
    first_name = db.Column(db.String(128), nullable=False)
    last_name = db.Column(db.String(128), nullable=False)
    birthdate = db.Column(db.Date, nullable=False)
    avatar_url = db.Column(db.String(1024), default=None)
    pw_hash = db.Column(db.String(128), nullable=False)
    locked = db.Column(db.Boolean, default=False, nullable=False)
    deleted = db.Column(db.Boolean, default=False, nullable=False)
    gender = db.Column(db.Enum(Gender), default=None)
    role_id = db.Column(
        db.Integer,
        ForeignKey('roles.id', onupdate='CASCADE'),
        nullable=False
    )

    role = db.relationship("Role", back_populates="users")
    channels = db.relationship("Channel", back_populates="user")

    def get_user_id(self):
        return self.id

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pw_hash, password)


class Client(db.Model, OAuth2ClientMixin, BaseMixin):
    __tablename__ = 'clients'
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE', onupdate='CASCADE'))
    trusted = db.Column(db.Boolean, default=False, nullable=False)
    user = db.relationship('User')


class Token(db.Model, OAuth2TokenMixin):
    __tablename__ = 'tokens'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE', onupdate='CASCADE'))
    user = db.relationship('User')

    def is_refresh_token_expired(self):
        expires_at = self.issued_at + self.expires_in * 2
        return expires_at < time.time()


class AuthorizationCode(db.Model, OAuth2AuthorizationCodeMixin):
    __tablename__ = 'authorization_codes'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey('users.id', ondelete='CASCADE', onupdate='CASCADE')
    )
    user = db.relationship('User')


class Channel(db.Model, BaseMixin):
    __tablename__ = 'channels'
    name = db.Column(db.String(32), nullable=False)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='CASCADE', onupdate='CASCADE'),
        nullable=False
    )
    description = db.Column(db.String(256), nullable=True)

    user = db.relationship('User', back_populates='channels')
    members = db.relationship('ChannelMember', back_populates='channel')


class ChannelMember(db.Model):
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='CASCADE', onupdate='CASCADE'),
        primary_key=True
    )
    channel_id = db.Column(
        db.Integer,
        db.ForeignKey('channels.id', ondelete='CASCADE', onupdate='CASCADE'),
        primary_key=True
    )
    created_at = db.Column('created_at', db.DateTime, default=datetime.now, nullable=False)

    user = db.relationship('User')
    channel = db.relationship('Channel', back_populates='members')


def init_app(app):
    with app.app_context():
        db.init_app(app)
        db.create_all()
        db.session.commit()
