import os, secrets
import pdfkit

# define base directory of app
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
	# key for CSF
	SECRET_KEY = os.environ.get('SECRET_KEY') or secrets.token_hex(32)
	# sqlalchemy .db location (for sqlite)
	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
	# sqlalchemy track modifications in sqlalchemy
	#Even though this is not used without stating it a warning is stated when run the website 
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	MAIL_SERVER = os.environ.get('MAIL_SERVER')
	MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
	MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
	MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
	MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
	ADMINS = ['email@email.com']
