from flask import Blueprint, render_template, flash, \
                redirect, url_for, request, session, make_response, current_app
from app.apps.forms import AddApplicationForm, EditApplicationForm, NoteForm, RejectedForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, TasterDay, Application, ApplicationType, Note, RejectedApplication
from app import db
from werkzeug.urls import url_parse
from sqlalchemy.sql import func, or_
from app.apps.email import send_application_email ,send_success_email, send_reject_email, send_edit_email, send_reject_reason_email
from app.models import User, requires_roles
import pdfkit 


apps = Blueprint('apps', __name__) 


@apps.route('/rejectApp/<id>', methods=['GET', 'POST'])
@login_required
def get_rejectApp(id):
    rejectApp = RejectedApplication.query.get(id)
    
    
    return render_template('apps/rejected_application.html', title="Rejected application", rejectApp=rejectApp)



@apps.route('/delete_app/<id>/<email>', methods=['GET', 'POST'])
@login_required
def delete_app(id,email):
    
    
    if Application.query.filter_by(id=id,email=email).delete():
        
        db.session.commit()
        send_reject_email(email)
        flash ('application has been deleted', 'success')
        return redirect(url_for('main.index'))

@apps.route('/success_app/<id>/<email>', methods=['GET', 'POST'])
@login_required
def success_app(id,email):
    
    
    if Application.query.filter_by(id=id,email=email):
        
        db.session.commit()
        send_success_email(email)
        flash ('email has been send', 'success')
        return redirect(url_for('main.index'))



@apps.route('/application/<id>', methods=['GET', 'POST'])
@login_required
def get_application(id):
    application = Application.query.get(id)
    form = NoteForm()
    if form.validate_on_submit():
        note = Note(
            text = form.text.data,
            user_id = current_user.get_id(),
            application_id = id
            )
        flash("Note has been added", "success")
        db.session.add(note)
        db.session.commit()
        return redirect(url_for('apps.get_application', id=id))
    
    
    return render_template('apps/application.html', title=application.last_name.title(), application=application, form=form)

@apps.route('/get_user_application/<id>/<id2>', methods=['GET', 'POST'])
@requires_roles('applicant')
@login_required
def get_user_application(id, id2):
    form = NoteForm()
    
    application = Application.query.filter_by(id=id, user_id=current_user.get_id()).count()
    if application == 0:
        flash("This is not your application and access is not granted", "danger")
        return redirect(url_for('main.index'))
        
    else: application = Application.query.filter_by(id=id, user_id=current_user.get_id()).first()
    form = NoteForm()
    if form.validate_on_submit():
        note = Note(
            text = form.text.data,
            user_id = current_user.get_id(),
            application_id = id
            )
        flash("Note has been added", "success")
        db.session.add(note)
        db.session.commit()
        return redirect(url_for('apps.get_application', id=id))  
    return render_template('apps/application.html', title="Application", application=application, form=form)




@apps.route('/new_app/', methods=['GET', 'POST'])
@requires_roles('applicant', 'admin')
@login_required
def new_app():
    form = AddApplicationForm()
    form.applicationtype_id.choices = [(c.id, c.name.title()) for c in ApplicationType.query.all()]
    if form.validate_on_submit():
        app = Application.query.filter_by(user_id=current_user.get_id()).count()
        if app != 0:
            flash("Already submitted an application", "warning")
            return redirect(url_for('main.index'))
        else:
            application = Application(
                
            
                    user_id = current_user.get_id(),
                    first_name= current_user.first_name,
                    last_name=current_user.last_name,
                    email=current_user.email,
                    
                                

                    interbac=form.interbac.data,
                    ielits=form.ielits.data,
                    gcse=form.gcse.data,
                    gcse2=form.gcse2.data,
                    gcse3=form.gcse3.data,
                    gcse3_grade=form.gcse3_grade.data,
                    gcse4=form.gcse4.data,
                    gcse4_grade=form.gcse4_grade.data,
                    gcse5=form.gcse5.data,
                    gcse5_grade=form.gcse5_grade.data,
                    ucas=form.ucas.data,
                    qaa=form.qaa.data,
                    company=form.company.data,
                    description=form.description.data,
                    start_date=form.start_date.data,
                    end_date=form.end_date.data,
                    personal_statement=form.personal_statement.data,
                    applicationtype_id=form.applicationtype_id.data,
                    tasterday_id=0
                  
                
            
        )
        db.session.add(application)
        db.session.flush()
        new_id = application.id
        db.session.commit()
        send_application_email(application)
        flash('application was added successfully', 'success')
        #return redirect(url_for('main.index'))
        return redirect(url_for('apps.get_application', id=new_id))
    return render_template('apps/new_app.html', title='Add Application', form=form)

@apps.route('/edit_app/<id>', methods=['GET', 'POST'])
@requires_roles('admin')
@login_required
def edit_app(id):
    application = Application.query.get(id)
    form = EditApplicationForm(obj=application)
    form.tasterday_id.choices = [(c.id, c.title.title()) for c in TasterDay.query.all()] 
    if request.method == 'GET':
        form.populate_obj(application)
    elif request.method == 'POST':
        if form.update.data and form.validate_on_submit():
            application.tasterday_id = form.tasterday_id.data

            db.session.commit()
            send_edit_email(application)
            flash ('Applicant was successful added to TasterDay', 'success')
            return redirect(url_for('apps.get_application', id=id))
        if form.cancel.data:
            return redirect(url_for('apps.get_application', id=id))
    return render_template('apps/edit_app.html', title='Edit app', form=form)



@apps.route('/reject_app/<id>/<email>/<first_name>/<last_name>', methods=['GET', 'POST'])
@requires_roles('admin')
@login_required
def reject_app(id,first_name,last_name,email):
    
    form = RejectedForm()
    if form.validate_on_submit():
        app = RejectedApplication.query.filter_by(application_id=id).count()
        if app != 0:
            flash("Already recorded a reason for rejecting application", "danger")
            return redirect(url_for('main.index'))
        else:
        
            rejectApp = RejectedApplication (
                application_id=id,
                first_name=first_name,
                last_name=last_name,
                reason=form.reason.data,
                email=email
                
        ) 
        
        
                
        db.session.add(rejectApp)
        db.session.flush()
        new_id = rejectApp.id
        db.session.commit()
        send_reject_reason_email(rejectApp)
            
        flash ('Applicant was successful added to rejected records', 'success')
        return redirect(url_for('apps.get_application', id=id)) 
        #return redirect(url_for('main.index', id=new_id, first_name=first_name, last_name=last_name, email=email))
    return render_template('apps/reject_app.html', title='reject app', form=form)





@apps.route('/delete_reject_record/<id>/', methods=['GET', 'POST'])
@login_required
@requires_roles('admin')
def delete_reject_record(id):
    
    
    if RejectedApplication.query.filter_by(id=id).delete():
        
        db.session.commit()
        
        flash ('application has been deleted', 'success')
        return redirect(url_for('main.index'))





@apps.route('/apps/<id>/edit_note', methods=['GET', 'POST'])
@requires_roles('admin')
@login_required
def edit_note(id):
    note = Note.query.filter_by(application_id=id, user_id=current_user.get_id())[0]
    form = NoteForm()
    if request.method == 'GET':
        form.text.data = note.text 
    if form.validate_on_submit() and request.method == 'POST':
        note.text = form.text.data
        db.session.commit()
        return redirect(url_for('apps.get_application', id=id)) 
    return render_template('apps/edit_note.html', title="Edit note", form=form, id=id)

@apps.route('/apps/<id1>/delete_note/<id2>', methods=['GET', 'POST'])
@requires_roles('admin')
@login_required
def delete_note(id1, id2):
    if Note.query.filter_by(id=id2).delete():
        db.session.commit()
        flash ('Note has been deleted', 'success')
        return redirect(url_for('apps.get_application', id=id1))
    return redirect(url_for('apps.get_application', id=id1))  

    



@apps.route('/reject_search', methods=['GET', 'POST'])
@login_required
def reject_search():
    rejectApps = None
    target_string = request.form['search']

    rejectApps = RejectedApplication.query.filter(
        or_(
            
            RejectedApplication.last_name.contains(target_string)
           
            )
        ).all()

    if target_string == '':
       
        
        search_msg = f'No record(s) found - displaying rejected all {len(rejectApps)} records'
        color = 'danger'
    else:
        search_msg = f'{len(rejectApps)} rejected application(s) found'
        color = 'success'
    return render_template('apps/reject_search.html', 
        title='Search result', rejectApps=rejectApps, 
        search_msg=search_msg, color=color
    )