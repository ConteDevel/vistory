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

TESTING = getenv('VIFS_TESTING', False)
DEBUG = getenv('VIFS_DEBUG', False)
SERVER_NAME = getenv('VIFS_SERVER_NAME', 'fs.vistory.local')
SECRET_KEY = getenv('VIFS_SECRET_KEY', 'secret')

"""
    DATABASE SETTINGS
"""
"""
    Connect to the following signals to get notified before and after changes 
    are committed to the database. These changes are only tracked if 
    SQLALCHEMY_TRACK_MODIFICATIONS is enabled in the config.
"""
SQLALCHEMY_TRACK_MODIFICATIONS = False
"""
    PostgreSQL connection settings
"""
DATABASE = {
    'HOST': getenv('VIFS_DB_HOST', 'localhost'),
    'PORT': getenv('VIFS_DB_PORT', '5432'),
    'USER': getenv('VIFS_DB_USER', 'postgres'),
    'PASSWORD': getenv('VIFS_DB_PASSWORD', '12345'),
    'NAME': getenv('VIFS_DB_NAME', 'vifs')
}
SQLALCHEMY_DATABASE_URI = 'postgresql://%(USER)s:'\
        '%(PASSWORD)s@%(HOST)s:%(PORT)s/%(NAME)s' % DATABASE
"""
    FILE UPLOADING
"""
IMG_ALLOWED_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.gif', '.svg'}
VIDEO_ALLOWED_EXTENSIONS = {'.mp4'}
