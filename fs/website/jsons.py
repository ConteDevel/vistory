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


class FileJsonMixin:

    def __init__(self, file, url):
        self.id = file.id
        self.created_at = file.created_at
        self.updated_at = file.updated_at
        self.url = url


class ImageJson(BaseJson, FileJsonMixin):

    def __init__(self, image, url):
        BaseJson.__init__(self, 'image')
        FileJsonMixin.__init__(self, image, url)


class VideoJson(BaseJson, FileJsonMixin):

    def __init__(self, image, url):
        BaseJson.__init__(self, 'video')
        FileJsonMixin.__init__(self, image, url)
