from flask_restful import Api

from website.routes import front, oauth2
from website.routes.api import MeRoutes

api = Api(prefix='/api')


def init_app(app):
    # Initialize routes
    app.register_blueprint(oauth2.bp)
    app.register_blueprint(front.bp)
    api.add_resource(MeRoutes, '/users/me')
    api.init_app(app)
