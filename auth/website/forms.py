from flask_wtf import RecaptchaField
from wtforms import Form, StringField, validators, PasswordField, DateField, SelectField
from wtforms.fields.html5 import EmailField
from wtforms.widgets.html5 import DateInput

from website.models import User, Gender


class SignUpForm(Form):
    first_name = StringField('First name', [
        validators.DataRequired(),
        validators.Length(min=3, max=64)
    ])
    last_name = StringField('Last name', [
        validators.DataRequired(),
        validators.Length(min=3, max=64)
    ])
    email = EmailField('Email', [
        validators.DataRequired(),
        validators.Length(min=6, max=255)
    ])
    birthdate = DateField('Date of Birth', [validators.DataRequired()], widget=DateInput())
    gender = SelectField('Gender', choices=[
        ('1', Gender.Male.name),
        ('0', Gender.Female.name)
    ])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.Length(min=8, max=50),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat password', [validators.DataRequired()])
    recaptcha = RecaptchaField()

    def to_user(self):
        user = User()
        user.email = self.email.data,
        user.name = self.name.data,
        user.birthdate = self.birthdate.data
        user.gender = Gender.Male if self.gender.data == '0' else Gender.Female
        user.set_password(password=self.password.data)
        return user

