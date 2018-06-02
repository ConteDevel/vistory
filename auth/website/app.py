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
from flask import Flask

from website import settings
from .models import db
from .oauth2 import config_oauth
from .routes import bp


def create_app(config=None):
    app = Flask(__name__)

    # load configuration
    app.config.from_object('website.settings')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(USER)s:'\
        '%(PASSWORD)s@%(HOST)s:%(PORT)s/%(NAME)s' % settings.DATABASE

    # load app specified configuration
    if config is not None:
        if isinstance(config, dict):
            app.config.update(config)
        elif config.endswith('.py'):
            app.config.from_pyfile(config)

    setup_app(app)
    return app


def setup_app(app):
    db.init_app(app)
    config_oauth(app)
    app.register_blueprint(bp, url_prefix='')
