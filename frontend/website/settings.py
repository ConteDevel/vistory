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
from os import getenv

SECRET_KEY = getenv('VIFRONTEND_SECRET_KEY', 'secret')
AUTHLIB_INSECURE_TRANSPORT=getenv('AUTHLIB_INSECURE_TRANSPORT', '0')
SQLALCHEMY_TRACK_MODIFICATIONS = False
SERVER_NAME = '127.0.0.1:5000'

DATABASE = {
    'HOST': getenv('VIFRONTEND_DB_HOST', 'localhost'),
    'PORT': getenv('VIFRONTEND_DB_PORT', '5432'),
    'USER': getenv('VIFRONTEND_DB_USER', 'postgres'),
    'PASSWORD': getenv('VIFRONTEND_DB_PASSWORD', '12345'),
    'NAME': getenv('VIFRONTEND_DB_NAME', 'vifrontend')
}

RECAPTCHA_PUBLIC_KEY = getenv('VIFRONTEND_RECAPTCHA_PUBLIC_KEY', '')
RECAPTCHA_PRIVATE_KEY = getenv('VIFRONTEND_RECAPTCHA_PRIVATE_KEY', '')
