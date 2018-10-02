from website.jsons.base import BaseJson


class ErrorJson(BaseJson):

    def __init__(self, code, error, messages):
        BaseJson.__init__(self, 'error')
        self.code = code
        self.error = error
        self.description = messages


class BadRequestJson(ErrorJson):

    def __init__(self, messages):
        ErrorJson.__init__(self, 400, 'BAD_REQUEST', messages)


class NotFoundJson(ErrorJson):

    def __init__(self, messages):
        ErrorJson.__init__(self, 404, 'NOT_FOUND', messages)


class UnprocessableEntityJson(ErrorJson):

    def __init__(self, messages):
        ErrorJson.__init__(self, 422, 'UNPROCESSABLE_ENTITY', messages)


class InternalServerErrorJson(ErrorJson):

    def __init__(self, messages):
        ErrorJson.__init__(self, 500, 'INTERNAL_SERVER_ERROR', messages)
