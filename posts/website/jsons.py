from datetime import date, time

from flask import json


def serialize(obj):
    if isinstance(obj, date):
        serial = obj.isoformat()
        return serial
    if isinstance(obj, time):
        serial = obj.isoformat()
        return serial
    return obj.__dict__


class BaseJson:

    def __init__(self, t):
        self.type = t

    def to_json(self):
        return json.dumps(self.__dict__, default=serialize)


class ErrorJson(BaseJson):

    def __init__(self, code, error, description):
        BaseJson.__init__(self, 'error')
        self.code = code
        self.error = error
        self.description = description


class BadRequestJson(ErrorJson):

    def __init__(self, description):
        ErrorJson.__init__(self, 400, 'BAD_REQUEST', description)


class NotFoundJson(ErrorJson):

    def __init__(self, description):
        ErrorJson.__init__(self, 404, 'NOT_FOUND', description)


class PostJson(BaseJson):

    def __init__(self, post):
        BaseJson.__init__(self, 'post')
        self.id = post.id
        self.created_at = post.created_at
        self.updated_at = post.updated_at
        self.description = post.description
        self.type = post.type.name.lower()
        self.attachment_id = post.attachment_id
        self.user_id = post.user_id
        self.blocked = post.blocked


class ChannelPostJson(PostJson):

    def __init__(self, post):
        PostJson.__init__(self, post)
        self.channel_id = post.channel_id
