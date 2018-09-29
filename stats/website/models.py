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

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class BaseMixin(object):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_at = db.Column('created_at', db.DateTime, default=datetime.now, nullable=False)


class Client(db.Model, BaseMixin):
    __tablename__ = 'clients'
    user_id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String, nullable=False)
    location = db.Column(db.String, nullable=True)


class Metric(db.Model, BaseMixin):
    __tablename__ = 'metrics'
    user_id = db.Column(db.Integer, nullable=False)
    action = db.Column(db.String, nullable=False)
    duration = db.Column(db.BigInteger, nullable=False, default=0)
    result = db.Column(db.String, nullable=False)


def init_db(app):
    with app.app_context():
        db.init_app(app)
        db.create_all()
        db.session.commit()
