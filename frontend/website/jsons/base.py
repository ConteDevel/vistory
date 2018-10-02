from datetime import date, time

from flask import json

from website.models import Gender


def serialize(obj):
    if isinstance(obj, Gender):
        return obj.name
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

