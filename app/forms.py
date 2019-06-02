from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FileField
from wtforms.validators import ValidationError, DataRequired, EqualTo
from app.models import User


class PasswordForm(FlaskForm):
    password = PasswordField('New Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class UploadForm(FlaskForm):
    file = FileField('File')
    submit = SubmitField('Upload')


class AddUserForm(PasswordForm):
    username = StringField('Username', validators=[DataRequired()])
    is_admin = BooleanField('Admin')
    submit = SubmitField('Add User')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')


class SearchForm(FlaskForm):
    file_name = StringField('File name')
    search = SubmitField('Search')


class ChangePasswordForm(PasswordForm):
    old_password = PasswordField('Old Password', validators=[DataRequired()])
    submit = SubmitField('Change Password')
