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
from flask import Flask
from flask_restful import Api
from models import FileUpload

app = Flask(__name__)
app.config.from_object("config")
api = Api(app)


api.add_resource(FileUpload, '/files/new')


# @app.route('/')
# def index():
#    return render_template('index.html')


# @app.route("/", methods=["POST"])
# def upload_file():
#     if "user_file" not in request.files:
#         return "No user_file key in request.files"
#     file = request.files["user_file"]
#     if file.filename == "":
#         return "Please select a file"
#     if file:
#         file.filename = secure_filename(file.filename)
#         output = helpers.upload_file_to_s3(file, app.config["AWS_S3_BUCKET"])
#         return str(output)
#     else:
#         return redirect("/")


if __name__ == "__main__":
    app.run()
