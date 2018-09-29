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
from flask import Blueprint

from website.oauth2 import server, current_user
from website.routes.base import login_required


bp = Blueprint('oauth', __name__)


@bp.route("/authorize", methods=['GET'])
@login_required
def authorize():
    user = current_user()
    return server.create_authorization_response(grant_user=user)


@bp.route('/token', methods=['POST'])
def issue_token():
    return server.create_token_response()


@bp.route('/revoke', methods=['POST'])
def revoke_token():
    return server.create_endpoint_response('revocation')
