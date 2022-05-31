from flask import render_template, current_app
from app.email import send_email
from threading import Thread
from flask import current_app
from flask_mail import Message
from app import mail
from app.models import TasterDay

APP_NAME = 'FYC'

