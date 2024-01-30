from flask_wtf import Form
from wtforms import StringField, PasswordField, validators


class RegistrationForm(Form):
    username = StringField('Username: ', [validators.DataRequired('Please input username')])
    password = PasswordField("Password: ", [validators.DataRequired("Please input password")])
    password2 = PasswordField("Input password again: ", [validators.EqualTo("password", message="Twice Input Password Mismatch")])
    fullname = StringField("Full name: ", [validators.DataRequired("Please input Full name")])
