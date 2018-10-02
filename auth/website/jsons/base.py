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


class PageJson(BaseJson):

    def __init__(self, json_type, page, pages):
        BaseJson.__init__(self, json_type)
        self.items = []
        self.page = page
        self.pages = pages


class UserJson(BaseJson):

    def __init__(self, user):
        BaseJson.__init__(self, 'user')
        self.id = user.id
        self.first_name = user.first_name
        self.last_name = user.last_name
        self.email = user.email
        self.gender = user.gender


class UserPageJson(PageJson):

    def __init__(self, users, page, pages):
        PageJson.__init__(self, 'users', page, pages)
        self.page = page
        self.pages = pages
        for user in users:
            self.items.append(UserJson(user))

