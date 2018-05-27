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
from config import AWS_S3_BUCKET
from flask_api import status
from flask_restful import Resource, reqparse
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
import helpers


class FileUpload(Resource):

    def post(self):
        parse = reqparse.RequestParser()
        parse.add_argument('user_file', type=FileStorage, location='user_file')
        parse.add_argument('user_id', type=int, location='user_id')
        args = parse.parse_args()
        file = args['user_file']
        if file:
            file.filename = secure_filename(file.filename)
            url = helpers.upload_file_to_s3(file, AWS_S3_BUCKET)
            return {'url': url}, status.HTTP_201_CREATED

        return 'Invalid file', status.HTTP_400_BAD_REQUEST
