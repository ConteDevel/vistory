from flask_restful import Api

from website.routes import front, oauth2
from website.routes.api import MeRoutes, UserListRoutes

api = Api(prefix='/api')


def init_app(app):
    # Initialize routes
    app.register_blueprint(oauth2.bp)
    app.register_blueprint(front.bp)
    api.add_resource(MeRoutes, '/users/me')
    api.add_resource(UserListRoutes, '/users')
    api.init_app(app)
