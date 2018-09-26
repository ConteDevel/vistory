from flask_wtf import RecaptchaField
from wtforms import Form, StringField, validators, PasswordField, DateField, SelectField, BooleanField, HiddenField
from wtforms.fields.html5 import EmailField, TelField
from wtforms.widgets.html5 import DateInput

from website.models import User, Gender, Client


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
    phone_number = TelField('Phone number', [
        validators.DataRequired(),
        validators.Length(min=5, max=15)
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
        user.first_name = self.first_name.data
        user.last_name = self.last_name.data
        user.phone_number = self.phone_number.data
        user.birthdate = self.birthdate.data
        user.gender = Gender.Male if self.gender.data == '0' else Gender.Female
        user.set_password(password=self.password.data)
        return user


class SignInForm(Form):
    email = EmailField('Email', [
        validators.DataRequired(),
        validators.Length(min=6, max=255)
    ])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.Length(min=8, max=50)
    ])
    recaptcha = RecaptchaField()
    next = HiddenField('Next URL')


class ClientForm(Form):
    name = StringField('Client name', [
        validators.DataRequired(),
        validators.Length(min=3, max=64)
    ])
    uri = StringField('Client URI', [
        validators.DataRequired(),
        validators.Length(min=6, max=1024)
    ])
    redirect_uri = StringField('Redirect URI', [
        validators.DataRequired(),
        validators.Length(min=6, max=1024)
    ])

    def to_client(self):
        client = Client()
        client.client_name = self.name.data
        client.client_uri = self.uri.data
        client.redirect_uri = self.redirect_uri.data
        return client
