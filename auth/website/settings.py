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

DATABASE = {
    'HOST': getenv('VIAUTH_DB_HOST', 'localhost'),
    'PORT': getenv('VIAUTH_DB_PORT', '5432'),
    'USER': getenv('VIAUTH_DB_USER', 'postgres'),
    'PASSWORD': getenv('VIAUTH_DB_PASSWORD', '12345'),
    'NAME': getenv('VIAUTH_DB_NAME', 'viauth')
}
