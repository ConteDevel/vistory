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


class PageMixin(object):

    def __init__(self, page, pages):
        self.items = []
        self.page = page
        self.pages = pages


class StatJsonMixin:

    def __init__(self, a_id, a_user_id, a_created_at):
        self.id = a_id
        self.user_id = a_user_id
        self.created_at = a_created_at


class ClientJson(BaseJson, StatJsonMixin):

    def __init__(self, client):
        BaseJson.__init__(self, 'client')
        StatJsonMixin.__init__(self, client.id, client.user_id, client.created_at)
        self.name = client.name
        self.location = client.location


class MetricJson(BaseJson, StatJsonMixin):

    def __init__(self, metric):
        BaseJson.__init__(self, 'metric')
        StatJsonMixin.__init__(self, metric.id, metric.user_id, metric.created_at)
        self.action = metric.action
        self.duration = metric.duration
        self.result = metric.result


class ClientsJson(BaseJson, PageMixin):

    def __init__(self, clients, page, pages):
        BaseJson.__init__(self, 'clients')
        PageMixin.__init__(self, page, pages)
        for client in clients:
            self.items.append(ClientJson(client))


class MetricsJson(BaseJson, PageMixin):

    def __init__(self, clients, page, pages):
        BaseJson.__init__(self, 'metrics')
        PageMixin.__init__(self, page, pages)
        for client in clients:
            self.items.append(ClientJson(client))
