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
from flask import Flask, render_template, request, redirect
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config.from_object('flask_s3_upload.conf')

from .helpers import *

@app.route('/')
def index():
    return render_template('index.html')


@app.route("/", methods=["POST"])
def upload_file():
    # A
    if "user_file" not in request.files:
        return "No user_file key in request.files"
    # B
    file    = request.files["user_file"]
    """
        These attributes are also available

        file.filename               # The actual name of the file
        file.content_type
        file.content_length
        file.mimetype

    """
    # C.
    if file.filename == "":
        return "Please select a file"
    # D.
    if file: # and allowed_file(file.filename):
        file.filename = secure_filename(file.filename)
        output        = upload_file_to_s3(file, app.config["S3_BUCKET"])
        return str(output)
    else:
        return redirect("/")

def upload_file_to_s3(file, bucket_name, acl="public-read"):
    try:
        s3.upload_fileobj(
            file,
            bucket_name,
            file.filename,
            ExtraArgs={
                "ACL": acl,
                "ContentType": file.content_type
            }
        )
    except Exception as e:
        print("Something Happened: ", e)
        return e
    return "{}{}".format(app.config["S3_LOCATION"], file.filename)

if __name__ == "__main__":
    app.run()
