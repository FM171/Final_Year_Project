from flask import render_template, current_app
from app.email import send_email
from app.models import Application, User

APP_NAME = 'Foundation Year in Computing'


def send_password_reset_email(user):
    token = user.get_reset_password_token()
    send_email(
        f'{APP_NAME} : Reset Your Password',
        sender=current_app.config['ADMINS'][0],
        recipients=[user.email],
        text_body=render_template(
            'email/reset_password.txt',
            user=user, token=token),
        html_body=render_template(
            'email/reset_password.html',
            user=user, token=token)
    )   
	


def send_registration_email(user):
    send_email(
        f'{APP_NAME} : Thank You For Registering',
        sender=current_app.config['ADMINS'][0],
        recipients=[user.email],
        text_body=render_template(
            'email/register_confirmation.txt',
            user=user),
        html_body=render_template(
            'email/register_confirmation.html',
            user=user)
    )


