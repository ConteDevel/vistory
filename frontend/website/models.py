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

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Gender(enum.Enum):
    Female = 0,
    Male = 1


class BaseMixin(object):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_at = db.Column('created_at', db.DateTime, default=datetime.now, nullable=False)
    updated_at = db.Column('updated_at', db.DateTime, default=datetime.now,
                           onupdate=datetime.now, nullable=False)


class User(db.Model, BaseMixin):
    __tablename__ = 'users'
    email = db.Column(db.String(255), nullable=False)
    phone_number = db.Column(db.String(15), nullable=False)
    first_name = db.Column(db.String(128), nullable=False)
    last_name = db.Column(db.String(128), nullable=False)
    birthdate = db.Column(db.Date, nullable=False)
    avatar_url = db.Column(db.String(1024), default=None)
    locked = db.Column(db.Boolean, default=False, nullable=False)
    deleted = db.Column(db.Boolean, default=False, nullable=False)
    gender = db.Column(db.Enum(Gender), default=None)
    friends = db.relationship('User', secondary=friends, lazy='subquery',
                              backref=db.backref('users', lazy=True))

    def get_user_id(self):
        return self.id


class Community(db.Model, BaseMixin):
    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(128), nullable=False)


friends = db.Table(
    'friends',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('friend_id', db.Integer, db.ForeignKey('users.id'), primary_key=True)
)


def init_db(app):
    with app.app_context():
        db.init_app(app)
        db.create_all()
        db.session.commit()
