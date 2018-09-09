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
import datetime

from authlib.flask.oauth2.sqla import OAuth2ClientMixin, OAuth2TokenMixin, OAuth2AuthorizationCodeMixin
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class BaseMixin(object):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column('created_at', db.DateTime, nullable=False)
    updated_at = db.Column('updated_at', db.DateTime, nullable=False)

    @staticmethod
    def create_time(mapper, connection, instance):
        now = datetime.datetime.utcnow()
        instance.created_at = now
        instance.updated_at = now

    @staticmethod
    def update_time(mapper, connection, instance):
        now = datetime.datetime.utcnow()
        instance.updated_at = now

    @classmethod
    def register(cls):
        db.event.listen(cls, 'before_insert', cls.create_time)
        db.event.listen(cls, 'before_update', cls.update_time)


class User(db.Model, BaseMixin):
    __tablename__ = 'users'
    email = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(512), nullable=False)
    birthdate = db.Column(db.Date, nullable=False)
    avatar_url = db.Column(db.String(1024))
    hash = db.Column(db.String(32), nullable=False)
    salt = db.Column(db.String(32), nullable=False)
    lock = db.Column(db.Boolean, default=False, nullable=False)
    deleted = db.Column(db.Boolean, default=True, nullable=False)

    def get_user_id(self):
        return self.id


class Client(db.Model, OAuth2ClientMixin, BaseMixin):
    __tablename__ = 'clients'
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE', onupdate='CASCADE'))
    user = db.relationship('User')


class Token(db.Model, OAuth2TokenMixin):
    __tablename__ = 'tokens'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE', onupdate='CASCADE'))
    user = db.relationship('User')


class AuthorizationCode(db.Model, OAuth2AuthorizationCodeMixin):
    __tablename__ = 'authorization_codes'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey('users.id', ondelete='CASCADE', onupdate='CASCADE')
    )
    user = db.relationship('User')
