from flask_wtf import RecaptchaField
from wtforms import Form, StringField, validators, PasswordField, DateField, SelectField, HiddenField
from wtforms.fields.html5 import EmailField, TelField
from wtforms.widgets.html5 import DateInput

from website.models import User, Gender, Client


class ProfileForm(Form):
    first_name = StringField('First name', [
        validators.DataRequired(),
        validators.Length(min=3, max=64)
    ])
    last_name = StringField('Last name', [
        validators.DataRequired(),
        validators.Length(min=3, max=64)
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

    def set(self, user):
        self.first_name.data = user.first_name
        self.last_name.data = user.last_name
        self.phone_number.data = user.phone_number
        self.birthdate.data = user.birthdate
        self.gender.data = '1' if user.gender == Gender.Male else '0'

    def to_user(self, user=None):
        if not user:
            user = User()
        user.first_name = self.first_name.data
        user.last_name = self.last_name.data
        user.phone_number = self.phone_number.data
        user.birthdate = self.birthdate.data
        user.gender = Gender.Male if self.gender.data == '1' else Gender.Female
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


class SignUpForm(ProfileForm, SignInForm):
    confirm = PasswordField('Repeat password', [validators.DataRequired()])

    def to_user(self, user=None):
        user = ProfileForm.to_user(self, user)
        user.email = self.email.data
        user.set_password(password=self.password.data)
        return user


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
