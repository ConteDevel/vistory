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
import enum
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class FileType(enum.Enum):
    Image = 0,
    Video = 1

    @staticmethod
    def from_value(value):
        if value == 'image':
            return FileType.Image
        if value == 'video':
            return FileType.Video
        raise ValueError('Post type can not be "%s".' % value)


class BaseMixin(object):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_at = db.Column(db.DateTime, default=datetime.now, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)


class Post(db.Model, BaseMixin):
    __tablename__ = 'posts'
    description = db.Column(db.String, nullable=True)
    user_id = db.Column(db.Integer, nullable=False)
    channel_id = db.Column(db.Integer, nullable=True)
    blocked = db.Column(db.Boolean, nullable=False, default=False)
    attachment_id = db.Column(db.Integer, nullable=False)
    type = db.Column(db.Enum(FileType), nullable=False)

    def parse(self, json_data):
        self.description = json_data.get('description', None)
        self.user_id = json_data['user_id']
        self.channel_id = json_data.get('channel_id', None)
        self.attachment_id = json_data['attachment_id']
        self.type = FileType.from_value(json_data['type'])


class PostLike(db.Model, BaseMixin):
    __tablename__ = 'likes'
    user_id = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now, nullable=False)
    post_id = db.Column(
        db.Integer,
        db.ForeignKey('posts.id', ondelete='CASCADE', onupdate='CASCADE'),
        nullable=False
    )


def init_app(app):
    with app.app_context():
        db.init_app(app)
        db.create_all()
        db.session.commit()
