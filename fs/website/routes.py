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
    along with Vistory.  If not, see <http://www.gnu.org/licenses/>.
"""
from flask_restful import Api, Resource

api = Api(prefix='/files')
logger = None


class ImageRoutes(Resource):
    def get(self):
        return {'hello': 'world'}


def init_routes(app):
    global logger
    logger = app.logger
    api.add_resource(ImageRoutes, '/')
    api.init_app(app)
