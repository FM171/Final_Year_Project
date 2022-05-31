from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms import TextAreaField, FileField, DecimalField, IntegerField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length, NumberRange, Regexp
from app.models import User
from flask_login import current_user

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    house_number = StringField('first line of address', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    post_code = StringField('Post Code', validators=[DataRequired()])
    country = StringField('Country ', validators=[DataRequired()])
    staffcode = StringField('staff_code', validators=[DataRequired(), EqualTo('role'  ,message='Wrong, please concact ... for help')])
    role = SelectField('Role', choices=[('applicant','applicant '),('admin','dmu_staff')], default=1)
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(),
                                           EqualTo('password')])
    submit = SubmitField('Request Password Reset')


class EditUserForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    house_number = StringField('first line of address', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    post_code = StringField('Post Code', validators=[DataRequired()])
    country = StringField('Country ', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    update = SubmitField('Update')
    cancel = SubmitField('Cancel')
    """
    stackoverflow answer that didnt work
    def clean_email(self):
        cd = self.cleaned_data
        email = cd(email=email.data)

        # object is exists and email is not modified, so don't start validation flow
        #if self.instance.pk is not None and self.instance.email == email:
        #    return cd

        # check email is unique or not
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address. This one is already registered to another account')
    """


