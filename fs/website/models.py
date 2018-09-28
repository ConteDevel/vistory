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
from os import path

from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename

db = SQLAlchemy()


class File(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_at = db.Column(db.DateTime, default=datetime.now, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)
    file = db.Column(db.LargeBinary, nullable=True)
    extension = db.Column(db.String, nullable=False)
    mime = db.Column(db.String, nullable=False)
    blocked = db.Column(db.Boolean, default=False, nullable=False)

    def __init__(self, file):
        _, ext = path.splitext(secure_filename(file.filename))
        self.file = file.read()
        self.extension = ext
        self.mime = file.content_type


class Image(File):
    __tablename__ = 'images'


class Video(File):
    __tablename__ = 'videos'


def init_db(app):
    with app.app_context():
        db.init_app(app)
        db.create_all()
        db.session.commit()
