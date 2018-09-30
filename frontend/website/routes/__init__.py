from website.routes import routes, oauth2


def init_app(app):
    # Initialize routes
    app.register_blueprint(oauth2.bp)
    app.register_blueprint(routes.bp)
