from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, BooleanField, SubmitField , TimeField, DateField
from wtforms import TextAreaField, FileField, DecimalField, IntegerField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length, NumberRange, Optional
from app.models import TasterDay, ApplicationType


class TasterDayForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(),Length(min=4, max=100)])
    date = DateField('Date', format='%d/%m/%Y')
    start_time = TimeField('Start Time')
    end_time = TimeField('End Time')
    location = StringField('Location', validators=[DataRequired(),Length(min=4, max=100)])
    
    
    submit = SubmitField('Add TasterDay')

    def validate_title(self, title):
        title = TasterDay.query.filter_by(title=title.data).first()
        if title is not None:
            raise ValidationError('Please use a different title as this on is already in use.')
    """
    def validate_participant_one(self, participant_one):
        tasterday = TasterDay.query.filter_by(participant_one=participant_one.data).first()
        if tasterday is not None:
            raise ValidationError('Please use a different email address. This one is already registered to Tasterday')
"""

class EditTasterDayForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(),Length(min=4, max=100)])
    date = DateField('Date', format='%d/%m/%Y')
    start_time = TimeField('Start Time')
    end_time = TimeField('End Time')
    location = StringField('Location', validators=[DataRequired(),Length(min=4, max=100)])
    update = SubmitField('Update')
    cancel = SubmitField('Cancel')





    
class ApplicationTypeForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(),Length(min=2, max=40)])
    submit = SubmitField('Submit')

    def validate_name(self, name):
        name = ApplicationType.query.filter_by(name=name.data).first()
        if name is not None:
            raise ValidationError('Please use a name as this one currently exists.')

class EditApplicationTypeForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(),Length(min=2, max=40)])
    update = SubmitField('Update')
    cancel = SubmitField('Cancel')
    



class ResponseForm(FlaskForm):
    text = TextAreaField('Respond by making a comment')
    submit = SubmitField('Submit')