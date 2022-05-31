from flask import Blueprint, render_template, flash, \
                redirect, url_for, request, session
from app.auth.forms import LoginForm, RegistrationForm, \
                            ResetPasswordForm,ResetPasswordRequestForm, EditUserForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Application
from app import db
from werkzeug.urls import url_parse
from app.auth.email import send_password_reset_email, send_registration_email
from app.models import User, requires_roles
from flask_login import current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password', 'danger')
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.index')
        flash("You are now signed in!", "success")
        return redirect(next_page)
    return render_template('auth/login.html', title='Login', form=form)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            house_number=form.house_number.data,
            city=form.city.data,
            post_code=form.post_code.data,
            country=form.country.data,
            staffcode=form.staffcode.data,
            role=form.role.data
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        send_registration_email(user)
        flash('Congratulations, you are now a registered user!', 'success')
        return(redirect(url_for('auth.login')))
    return render_template('auth/register.html', title='Register', form=form)


@auth.route('/logout', methods=['GET', 'POST'])
@requires_roles('admin','applicant')
@login_required
def logout():
    logout_user()
    session.clear()
    flash("You've signed out!", "success")
    return redirect(url_for('main.index'))

#fuction to reset password
@auth.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
            flash('Check your email for the instructions to reset your password', 'info')
            return redirect(url_for('auth.login'))
        else:
            flash('An error occured, please try again', 'danger')
            return redirect(url_for('main.index'))
    return render_template('auth/reset_password_request.html',
                           title='Reset Password', form=form)

#creates token to access the fuction
@auth.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('main.index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form)


#Fuction allows thte user to edit acocunt details
@auth.route('/edit_user/<id>', methods=['GET', 'POST'])
@requires_roles('admin','applicant')
@login_required
def edit_user(id):
    user = User.query.get(id)
    form = EditUserForm(obj=user)
    if request.method == 'GET':
        form.populate_obj(user)
    elif request.method == 'POST':
        if form.update.data and form.validate_on_submit():
            user.first_name = form.first_name.data
            user.last_name = form.last_name.data
            user.set_password(form.password.data)
            user.email = form.email.data
            user.house_number=form.house_number.data
            city=form.city.data
            post_code=form.post_code.data
            country=form.country.data
            


            db.session.commit()
            flash ('Update was successful', 'success')
            return redirect(url_for('main.index', id=id))
        if form.cancel.data:
            return redirect(url_for('main.index', id=id))
    return render_template('auth/edit_user.html', title='edit_useruser', form=form)


# This fuction checks if user has a application and if not then allows the to delete the account
@auth.route('/delete_user/<id>/', methods=['GET', 'POST'])
@login_required
def delete_user(id):
    app = Application.query.filter_by(user_id=id).first()
    if app is not None:
        flash("Please withdraw your application then delete account", "danger")
        return redirect(url_for('main.index'))

    if User.query.filter_by(id=id).delete():
        db.session.commit()
        flash (' has been deleted', 'success')
        return(redirect(url_for('auth.login')))
    return render_template('auth/login.html', title='Login')



