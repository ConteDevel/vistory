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
import logging
from os import path

from flask import Flask

from website import routes, oauth2
from .models import init_db


def create_app(config=None):
    app = Flask(__name__)
    # load configuration
    if path.isfile('website/config/production.py'):
        app.config.from_object('website.config.production')
    else:
        app.config.from_object('website.config.default')
    # load app specified configuration
    if config is not None:
        if isinstance(config, dict):
            app.config.update(config)
        elif config.endswith('.py'):
            app.config.from_pyfile(config)
    setup_app(app)

    return app


def setup_app(app):
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
    init_db(app)
    oauth2.init_app(app)
    routes.init_app(app)

