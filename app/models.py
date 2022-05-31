import jwt
from time import time
from app import db, login
from datetime import datetime

from flask import current_app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from flask_login import current_user
from flask import Blueprint, render_template, flash, \
                redirect, url_for, request, session


# timestamp to be inherited by other class models
class TimestampMixin(object):
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)




class User(db.Model, TimestampMixin, UserMixin):
    __tablename__ = 'user'
    __table_args__ = {'extend_existing': True} #stops model from overiding existing table
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(80), nullable=False, unique=False)
    password_hash = db.Column(db.String(128))
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    admin = db.Column(db.Integer, default=0)
    note = db.relationship('Note', backref='user', lazy='dynamic') #creates relationship 
    staffcode =  db.Column(db.String(50), nullable=True, unique=False)
    role = db.Column(db.String(64), default='applicant')  
    house_number = db.Column(db.String(20), nullable=False)
    city  = db.Column(db.String(20), nullable=True)
    post_code  = db.Column(db.String(20), nullable=True)
    country = db.Column(db.String(20), nullable=False)  
    
    # generate user password i.e. hashing
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    # check user password is correct
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    # for reseting a user password
    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'],
            algorithm='HS256').decode('utf-8')
    # verify token generated for resetting password
    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)


class TasterDay(db.Model):
    __tablename__ = 'tasterday'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True) #stops model from overiding existing table
    title = db.Column(db.String(100), nullable=False, unique=False)
    date = db.Column(db.Date, nullable=False, unique=False)
    start_time = db.Column(db.Time, nullable=False, unique=False)
    end_time = db.Column(db.Time, nullable=False , unique=False)
    location = db.Column(db.String(100), nullable=False, unique=False)
    application = db.relationship('Application', backref='tasterday', lazy='dynamic') #creates relationship bewtween Appplication and TasterDay
    response = db.relationship('Response', backref='tasterday', lazy='dynamic')
    







        

class Application(db.Model):
    __table_args__ = {'extend_existing': True}
    _tablename__ = 'application'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(80), nullable=False, unique=False)
    personal_statement = db.Column(db.Text)
    applicationtype_id = db.Column(db.Integer, db.ForeignKey('applicationtype.id'))
    gcse = db.Column(db.String(50), nullable=True, unique=False)
    gcse2 = db.Column(db.String(50), nullable=True, unique=False)
    gcse3 = db.Column(db.String(50), nullable=True, unique=False)
    gcse3_grade = db.Column(db.String(50), nullable=True, unique=False)
    gcse4 = db.Column(db.String(50), nullable=True, unique=False)
    gcse4_grade = db.Column(db.String(50), nullable=True, unique=False)
    gcse5 = db.Column(db.String(50), nullable=True, unique=False)
    gcse5_grade = db.Column(db.String(50), nullable=True, unique=False)
    ucas = db.Column(db.Integer, nullable=True, unique=False)
    qaa = db.Column(db.String(4), nullable=True, unique=False)
    interbac = db.Column(db.Integer, nullable=True, unique=False)
    ielits = db.Column(db.Integer, nullable=True, unique=False)
    company = db.Column(db.String(20), nullable=True)
    description = db.Column(db.Text)
    start_date = db.Column(db.Date, nullable=True, unique=False)
    end_date = db.Column(db.Date, nullable=True, unique=False)
    note = db.relationship('Note', backref='application', lazy='dynamic')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    tasterday_id = db.Column(db.Integer, db.ForeignKey('tasterday.id'), nullable=True, unique=False)
    
    
    

    
 
class RejectedApplication(db.Model):
    __table_args__ = {'extend_existing': True}
    _tablename__ = 'rejectedApplication '
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), nullable=True)
    last_name = db.Column(db.String(20), nullable=True)
    reason = db.Column(db.String(80), nullable=True, unique=False)
    email = db.Column(db.String(80), nullable=True, unique=False)
    application_id = db.Column(db.Integer, db.ForeignKey('application.id'))
    
    

class ApplicationType(db.Model):
    __tablename__ = 'applicationtype'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False, unique=True)
    application = db.relationship('Application', backref='applicationtype', lazy='dynamic')



class Note(TimestampMixin, db.Model):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    application_id = db.Column(db.Integer, db.ForeignKey('application.id'))

 
   

class Response(TimestampMixin, db.Model):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    role = db.Column(db.String(20), nullable=True)
    tasterday_id = db.Column(db.Integer, db.ForeignKey('tasterday.id'))

  
@login.user_loader
def load_user(id):
    return User.query.get(int(id))

@login.user_loader
def load_user(id):
    return User.query.get(int(id))
    
def requires_roles(*roles):
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if current_user.role not in roles:
                flash ('Permission not granted', 'danger')
                return redirect(url_for('main.index'))
                # Redirect the user to an unauthorized notice!
               
            return f(*args, **kwargs)
        return wrapped
    return wrapper