from flask import render_template, current_app
from app.email import send_email
from app.models import Application

APP_NAME = 'Foundation Year in Computing'


def send_edit_email(application):
    send_email(
        f'{APP_NAME} : TasterDay update',
        sender=current_app.config['ADMINS'][0],
        recipients=[application.email],
        text_body=render_template(
            'email/edit_confirmation.txt',
            application=application),
        html_body=render_template(
            'email/edit_confirmation.html',
            application=application)
    )





def send_reject_reason_email(rejectApp):
    send_email(
        f'{APP_NAME} : Application update',
        sender=current_app.config['ADMINS'][0],
        recipients=[rejectApp.email],
        text_body=render_template(
            'email/reject_reason_confirmation.txt',
            rejectApp=rejectApp),
        html_body=render_template(
            'email/reject_reason_confirmation.html',
            rejectApp=rejectApp)
    )





def send_application_email(application):
    send_email(
        f'{APP_NAME} : Thank You For Application',
        sender=current_app.config['ADMINS'][0],
        recipients=[application.email],
        text_body=render_template(
            'email/application_confirmation.txt',
            application=application),
        html_body=render_template(
            'email/application_confirmation.html',
            application=application)
    )



        


def send_reject_email(email):
    send_email(
        f'{APP_NAME} : Application FYC update',
        sender=current_app.config['ADMINS'][0],
        recipients=[email],
        text_body=render_template(
            'email/reject_confirmation.txt',
            email=email),
        html_body=render_template(
            'email/reject_confirmation.html',
            email=email)
    )


def send_success_email(email):
    send_email(
        f'{APP_NAME} : Application FYC update',
        sender=current_app.config['ADMINS'][0],
        recipients=[email],
        text_body=render_template(
            'email/success_confirmation.txt',
            email=email),
        html_body=render_template(
            'email/success_confirmation.html',
            email=email)
    )