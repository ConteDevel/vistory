"""reqparse,
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
    along with Vistory. If not, see <http://www.gnu.org/licenses/>.
"""
from flask import render_template, redirect, request, Blueprint, current_app as app, url_for
from werkzeug.security import gen_salt

from website.forms import ClientForm
from website.models import Client, db
from website.oauth2 import current_user, GRANT_TYPES, RESPONSE_TYPES
from website.routes.base import login_required, admin_required


bp = Blueprint('front', __name__)


@bp.route('/')
@login_required
def home():
    user = current_user()
    if user.role.name == app.config['ADMIN_ROLE']:
        clients = Client.query.filter_by(user_id=user.id).all()
        form = ClientForm(request.form)
        return render_template("home.html", user=user, clients=clients, form=form)
    return render_template("home.html", user=user)


@bp.route('/create_client', methods=['POST'])
@admin_required
def create_client():
    form = ClientForm(request.form)
    if form.validate():
        user = current_user()
        client = form.to_client()
        client.user_id = user.id
        client.grant_types = GRANT_TYPES
        client.response_types = RESPONSE_TYPES
        client.client_id = gen_salt(24)
        client.client_secret = gen_salt(48)
        db.session.add(client)
        db.session.commit()
    return redirect(url_for('front.home'))
