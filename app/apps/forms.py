from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, BooleanField, SubmitField , TimeField, DateField
from wtforms import TextAreaField, FileField, DecimalField, IntegerField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length, NumberRange, Optional, Regexp, AnyOf
from app.models import Application, RejectedApplication

class AddApplicationForm(FlaskForm):
    
     #participant_one = StringField('participant one', validators=[Optional(), Email()])
    gcse = StringField('Math GCSE grade', validators=[Optional(), AnyOf(values=['C', 'B' , 'A', 'c', 'b', 'a', 'a*', 'A*'], message='A grade C and above is nedded to apply for this course', values_formatter=None)])
    gcse2 = StringField('English GCSE grade', validators=[Optional(), AnyOf(values=['C', 'B' , 'A', 'c', 'b', 'a', 'a*', 'A*'], message='A grade C and above is nedded to apply for this course', values_formatter=None)])
    gcse3 =  StringField(' third GCSEs title', validators=[Optional(),Length(min=2, max=50)])
    gcse3_grade = StringField('third GCSE grade',validators=[Optional(), AnyOf(values=['C', 'B' , 'A', 'c', 'b', 'a', 'a*', 'A*'], message='A grade C and above is nedded to apply for this course', values_formatter=None)])
    gcse4 =  StringField(' fourth GCSEs title', validators=[Optional(),Length(min=2, max=50)])
    gcse4_grade = StringField('fourth GCSE grade', validators=[Optional(), AnyOf(values=['C', 'B' , 'A', 'c', 'b', 'a', 'a*', 'A*'], message='A grade C and above is nedded to apply for this course', values_formatter=None)])
    gcse5 =  StringField(' fifth GCSEs title', validators=[Optional(),Length(min=2, max=50)])
    gcse5_grade = StringField('fifth GCSE grade',validators=[Optional(), AnyOf(values=['C', 'B' , 'A', 'c', 'b', 'a', 'a*', 'A*'], message='A grade C and above is nedded to apply for this course', values_formatter=None)])
    ucas = IntegerField('UCAS', validators=[Optional(), NumberRange(min=56, max=360, message='A minimum of 56 points is needed to apply for this course')])
      #staff_code = StringField('staff_code', validators=[DataRequired(), Regexp('iamstaff', flags=0, message='Wrong, please concact ... for help')])
    qaa = StringField('QAA', validators=[Optional(), AnyOf(values=['Pass', 'PASS', 'pass'], message='A Pass is nedded to apply for this course', values_formatter=None)])
    interbac = IntegerField('International Baccalaureate, Optional', validators=[Optional(), NumberRange(min=24, max=45, message='A minimum score of 24 is needed to apply for this course')]) 
    ielits = IntegerField('IELITS score', [Optional(),NumberRange(min=6, max=9,message='A minimum of score of 6 is needed to apply for this course' )])
    company = StringField('Company', validators=[Optional(),Length(min=2, max=100)])
    description = TextAreaField('Description', validators=[Optional(), Length(min=15, max=500)]) 
    start_date = DateField('Start Date', format='%m/%d/%Y', validators=(Optional(),))
    end_date = DateField('Start Date', format='%m/%d/%Y', validators=(Optional(),))
    #start_date = DateField('end Date', Optional(), format='%d/%m/%Y')
    #end_date = DateField('end Date', format='%d/%m/%Y')
    personal_statement = TextAreaField('Personal statement', validators=[DataRequired(), Length(min=25, max=500)])
    applicationtype_id= SelectField('Application type', coerce=int)
    name= StringField('Company', validators=[Optional(),Length(min=2, max=100)])
   #image = FileField('Add image', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Submit application') 

    def validate_fields(self):
        gcse= self.gcse.data
        gcse2 = self.gcse2.data
        gcse3_grade = self.gcse3_grade.data
        gcse4_grade = self.gcse4_grade.data
        gcse5_grade = self.gcse5_grade.data

        grades = (gcse, gcse2, gcse3_grade, gcse4_grade, gcse5_grade)

        if any(grades) is True:
            if all(grades) is False:
                raise ValidationError('Please enter 5 GCSE grades')


    
   
  
class EditApplicationForm(FlaskForm):
    tasterday_id = SelectField('TasterDay', coerce=int)
    #tasterday_id = SelectField('TasterDay', choices=[('coerce=int','coerce=int '),('0','None')], default=1)
    update = SubmitField('Update')
    cancel = SubmitField('Cancel')


    


class NoteForm(FlaskForm):
    text = TextAreaField('Make a note')
    submit = SubmitField('Submit')

class RejectedForm(FlaskForm):
    reason = TextAreaField('Reason why application is rejected')
    submit = SubmitField('Submit')  

    def validate_user_id(self, user_id):
        user_id = RejectedApplication.query.filter_by(user_id=user_id.data).first()
        if user_id is not None:
            raise ValidationError('Already submitted a reason.')

    def validate_user_id(self, email):
        email = RejectedApplication.query.filter_by(email=email.data).first()
        if email is not None:
            raise ValidationError('Already submitted a reason.')



 