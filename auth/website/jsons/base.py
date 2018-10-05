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


class EntityJson(BaseJson):

    def __init__(self, e_type, entity):
        BaseJson.__init__(self, e_type)
        self.id = entity.id
        self.created_at = entity.created_at
        self.updated_at = entity.updated_at


class UserJson(EntityJson):

    def __init__(self, user):
        EntityJson.__init__(self, 'user', user)
        self.first_name = user.first_name
        self.last_name = user.last_name
        self.email = user.email
        self.phone_number = user.phone_number
        self.birthdate = user.birthdate
        self.gender = user.gender
        self.role = user.role.name


class ChannelJson(EntityJson):

    def __init__(self, channel):
        EntityJson.__init__(channel, 'channel', channel)
        self.name = channel.name
        self.description = channel.description
        self.user_id = channel.user_id
        self.members = channel.num_members


class UserPageJson(PageJson):

    def __init__(self, users, page, pages):
        PageJson.__init__(self, 'users', page, pages)
        self.page = page
        self.pages = pages
        for user in users:
            self.items.append(UserJson(user))


class ChannelPageJson(PageJson):

    def __init__(self, channels, page, pages):
        PageJson.__init__(self, 'channels', page, pages)
        for channel in channels:
            self.items.append(ChannelJson(channel))
