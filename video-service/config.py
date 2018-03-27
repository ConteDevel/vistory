'''
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
'''
import os

S3_BUCKET   = os.environ['S3_BUCKET']
S3_KEY      = os.environ['S3_KEY']
S3_SECRET   = os.environ['S3_SECRET']
S3_LOCATION = 'http://{}.s3.amazonaws.com/'.format(S3_BUCKET)

SECRET_KEY  = os.random(32)
DEBUG       = True
PORT        = 5000
