from website.routes import account, oauth2, front, api


def init_app(app):
    # Initialize routes
    app.register_blueprint(account.bp, urlprefix='/account')
    app.register_blueprint(oauth2.bp, urlprefix='/oauth')
    app.register_blueprint(front.bp)
    api.init_app(app)
