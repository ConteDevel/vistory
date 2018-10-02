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

    def __init__(self, json_type):
        self.type = json_type

    def to_json(self):
        return json.dumps(self.__dict__, default=serialize)


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
        self.channel_id = post.channel_id
        self.likes = post.num_likes


class PageJson(BaseJson):

    def __init__(self, json_type, page, pages):
        BaseJson.__init__(self, json_type)
        self.items = []
        self.page = page
        self.pages = pages


class PostPageJson(PageJson):

    def __init__(self, posts, page, pages, user_id=None):
        PageJson.__init__(self, 'posts', page, pages)
        if user_id:
            self.user_id = user_id
        for post in posts:
            post_json = PostJson(post)
            self.items.append(post_json)


class LikeJson(BaseJson):

    def __init__(self, like):
        BaseJson.__init__(self, 'like')
        self.user_id = like.user_id
        self.post_id = like.post_id
        self.created_at = like.created_at
