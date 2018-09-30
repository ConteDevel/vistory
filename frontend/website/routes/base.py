import urllib.parse
from functools import wraps

from flask import url_for, request, redirect, current_app as app


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'Authorization' not in request.headers:
            back_url = urllib.parse.quote(url_for('bp.home', _external=True))
            url = "{0}?next={1}".format(app.config['AUTH_SERVICE'], back_url)
            return redirect(url)
        return f(*args, **kwargs)
    return decorated_function
