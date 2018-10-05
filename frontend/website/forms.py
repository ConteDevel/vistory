from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileAllowed
from wtforms import StringField, validators, HiddenField, FileField


class NewPostForm(FlaskForm):
    description = StringField('Description', [validators.Length(max=256)])
    file = FileField(validators=[
        FileRequired(),
        FileAllowed(['jpg', 'jpeg', 'png', 'mp4'], 'Images and videos only!')
    ])
    channel_id = HiddenField()


class NewChannelForm(FlaskForm):
    name = StringField('Name', [validators.Length(max=32)])
    description = StringField('Description', [validators.Length(max=256)])
