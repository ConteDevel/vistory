from website.routes import account, oauth2, front, api


def init_app(app):
    # Initialize routes
    app.register_blueprint(account.bp, url_prefix='/account')
    app.register_blueprint(oauth2.bp, url_prefix='/oauth')
    app.register_blueprint(front.bp)
    api.init_app(app)
