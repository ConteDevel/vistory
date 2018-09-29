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

TESTING = getenv('VIFRONT_TESTING', False)
DEBUG = getenv('VIFRONT_DEBUG', False)
SERVER_NAME = getenv('VIFRONT_SERVER_NAME', 'vistory.local')
SECRET_KEY = getenv('VIFRONT_SECRET_KEY', 'secret')

"""
    OAUTH 2.0 SETTINGS
"""
CLIENT_ID = getenv('VIFRONT_CLIENT_ID', '')
CLIENT_SECRET = getenv('VIFRONT_CLIENT_SECRET', '')

"""
    GOOGLE RECAPTCHA SETTINGS
"""
RECAPTCHA_PUBLIC_KEY = getenv('VIFRONT_RECAPTCHA_PUBLIC_KEY', '')
RECAPTCHA_PRIVATE_KEY = getenv('VIFRONT_RECAPTCHA_PRIVATE_KEY', '')

"""
    SERVICES
"""
AUTH_SERVICE = 'http://auth.vistory.local'
FS_SERVICE = 'http://fs.vistory.local'
POSTS_SERVICE = 'http://posts.vistory.local'
STATS_SERVICE = 'http://statistics.vistory.local'
