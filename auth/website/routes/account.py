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
from flask import request, render_template, session, redirect, Blueprint, url_for
from sqlalchemy import engine

from website.forms import SignUpForm, SignInForm, ProfileForm
from website.models import User, db, Gender
from website.oauth2 import current_user

bp = Blueprint('account', __name__)


@bp.route('/signin', methods=['GET', 'POST'])
def sign_in():
    form = SignInForm(request.form)
    next_url = request.args.get('next')
    if next_url:
        form.next.data = next_url
    if request.method == 'POST' and form.validate():
        email = form.email.data
        user = User.query.filter_by(email=email).first()
        if not (user and user.check_password(form.password.data)):
            render_template('account/sign_in.html', form=form,
                            error_msg='Invalid email or password')
        session['id'] = user.id
        next_url = form.next.data
        if next_url:
            return redirect(next_url)
        return url_for('front.home')
    return render_template('account/sign_in.html', form=form)


@bp.route('/signout')
def sign_out():
    del session['id']
    return redirect(url_for('account.sign_in'))


@bp.route('/signup', methods=['GET', 'POST'])
def sign_up():
    form = SignUpForm(request.form)
    next_url = request.args.get('next')
    if next_url:
        form.next.data = next_url
    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(email=form.email.data).first()
        if not user:
            user = form.to_user()
            db.session.add(user)
            db.session.commit()
            next_url = form.next.data
            sign_in_url = url_for('account.sign_in', next=next_url) if next_url \
                else url_for('account.sign_in')
            return redirect(sign_in_url)
    return render_template('account/sign_up.html', form=form)


@bp.route('/profile', methods=['GET', 'POST'])
def profile():
    user = current_user()
    form = ProfileForm(request.form)
    if request.method == 'GET':
        form.set(user)
    else:
        if form.validate():
            form.to_user(user)
            db.session.commit()
            db.session.flush()

    return render_template('account/profile.html', user=user, form=form)
