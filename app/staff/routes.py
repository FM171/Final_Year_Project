from flask import Blueprint, render_template, flash, \
                redirect, url_for, request, session, make_response, current_app
from app.staff.forms import TasterDayForm, EditTasterDayForm,  \
    ApplicationTypeForm, EditApplicationTypeForm, ResponseForm 
from app.apps.forms import AddApplicationForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, TasterDay, Application, ApplicationType, Response
from sqlalchemy.sql import func, or_
from werkzeug.urls import url_parse
from flask_paginate import Pagination, get_page_args
from app import db
from app.models import User, requires_roles
import pdfkit



staff = Blueprint('staff', __name__)

def all_tasterdays():
    return 'All tasterdays page'


@staff.route('/print_tasterday/<title>/<location>/<date>/<start_time>/<end_time>/', methods=['GET', 'POST'])
@requires_roles('admin', 'applicant')
@login_required
def pdf_template(title,location,start_time,end_time, date):
    rendered = render_template('pdf_template.html', title=title, location=location,start_time=start_time, end_time=end_time, date=date )
    pdf = pdfkit.from_string(rendered, False)

    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attatchment; filename=tasterday.pdf'

    return response





@staff.route('/search_pdf/', methods=['GET', 'POST'])
@requires_roles('admin')
@login_required
def pdf_search():

    tasterdays = TasterDay.query.order_by(TasterDay.id.asc())
    applications = Application.query.order_by(Application.tasterday_id.asc())
    rendered = render_template('pdf_search.html', applications=applications, tasterdays=tasterdays)
    pdf = pdfkit.from_string(rendered, False)

    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attatchment; filename=search.pdf'

    return response




@staff.route('/tasterday/<id>', methods=['POST', 'GET'])
@requires_roles('admin','applicant')
@login_required
def get_tasterday(id):
    if current_user.role == "applicant":
        roles= "Applicant"
    else:
        roles="Staff"
    tasterday = TasterDay.query.get(id)
    form = ResponseForm()
    if form.validate_on_submit():
        response = Response(
            text = form.text.data,
            user_id = current_user.get_id(),
            tasterday_id = id,  
            first_name= current_user.first_name,
            last_name=current_user.last_name,
            role=roles 
            )
        flash("Response has been added", "success")
        db.session.add(response)
        db.session.commit()
        return redirect(url_for('staff.get_tasterday', id=id))
    return render_template('staff/tasterday.html', title="TasterDay", tasterday=tasterday, form=form)





@staff.route('/get_user_tasterday/<id>/<tasterday_id>', methods=['GET', 'POST'])
@requires_roles('admin','applicant')
@login_required
def get_user_tasterday(id,tasterday_id):
    application = Application.query.get(id)
    tasterday = TasterDay.query.filter_by(id=application.tasterday_id).first()
    if application.tasterday_id == 0 or tasterday == None:
        flash("Not invited to TasterDay yet, please check again later", "warning")
        return redirect(url_for('apps.get_application', id=id))
    elif Application.query.filter_by(id=id,tasterday_id=tasterday_id):
        return redirect(url_for('staff.get_tasterday', id=tasterday_id))





@staff.route('/all_applications')
def all_applications():
    return 'All application page'


@staff.route('/new_tasterday', methods=['GET','POST'])
@requires_roles('admin')
@login_required
def new_tasterday():
    
   
            
    form = TasterDayForm()
   
    if form.validate_on_submit():
       
  
        tasterday = TasterDay(
            title=form.title.data,
            date=form.date.data,
            start_time=form.start_time.data,
            end_time=form.end_time.data,
            
            location=form.location.data,
           
        )
        
        

        db.session.add(tasterday)
        db.session.flush()
        new_id = tasterday.id
        db.session.commit()
        
       
        flash('Taster Day was added successfully', 'success')
        return redirect(url_for('main.index'))
    return render_template('staff/new_tasterday.html', title='Add TasterDay', form=form)




@staff.route('/edit_tasterday/<id>', methods=['GET', 'POST'])
@requires_roles('admin')
@login_required
def edit_tasterday(id):
    tasterday = TasterDay.query.get(id)
    form = EditTasterDayForm(obj=tasterday)
    if request.method == 'GET':
        form.populate_obj(tasterday)
    elif request.method == 'POST':
        if form.update.data and form.validate_on_submit():

            tasterday.title=form.title.data
            tasterday.date=form.date.data
            tasterday.start_time=form.start_time.data
            tasterday.end_time=form.end_time.data
            tasterday.location=form.location.data
           
          
            

            db.session.commit()           
            flash ('Update was successful', 'success')
            return redirect(url_for('staff.get_tasterday', id=id))
        if form.cancel.data:
            return redirect(url_for('main.index', id=id))
    return render_template('staff/edit_tasterday.html', title='Edit tasterday', form=form, tasterday=tasterday)




@staff.route('/remove_from_tasterday/<id>/<tasterday_id>', methods=['GET', 'POST'])
@requires_roles('admin')
@login_required
def remove_from_tasterday(id, tasterday_id):
    application = Application.query.filter_by(id=id).first()
    application.tasterday_id = 0
    db.session.commit()
    flash ('Application removed from TasterDay', 'success')
    return redirect(url_for('apps.get_application', id=id))
    








@staff.route('/delete_tasterday/<id>/', methods=['GET', 'POST'])
@requires_roles('admin')
@login_required
def delete_tasterday(id):

    app = Application.query.filter_by(tasterday_id=id).first()
    if app is not None:
        flash("Please remove all application form TasterDay then delete ", "danger")
        return redirect(url_for('main.index'))

    if TasterDay.query.filter_by(id=id).delete():
        db.session.commit()
        flash ('tasterday has been deleted', 'success')
        return redirect(url_for('main.index'))
    return redirect(url_for('main.index'))






@staff.route('/applicationtype', methods=['GET', 'POST'])
@requires_roles('admin')
@login_required
def applicationtype():
    form = ApplicationTypeForm()
    types = ApplicationType.query.order_by(ApplicationType.name.asc())
    if form.validate_on_submit():
        cat = ApplicationType(name = form.name.data)

        db.session.add(cat)
        db.session.commit()
        flash(f'{form.name.data} was added successfully', 'success')
        return redirect(url_for('staff.applicationtype'))

    return render_template(
        'staff/types.html', 
        title='Types', 
        types=types,
        form=form
    )

@staff.route('/edit_applicationtype/<id>', methods=['GET', 'POST'])
@requires_roles('admin')
@login_required
def edit_applicationtype(id):
    applicationtype = ApplicationType.query.get(id)
    form = EditApplicationTypeForm(obj=applicationtype)
    form.populate_obj(applicationtype)
    if request.method == 'POST':
       if form.update.data and form.validate_on_submit():
           applicationtype.name = form.name.data 
           db.session.commit()
           flash ('Update was successful', 'success')
           return redirect(url_for('staff.applicationtype'))
    if form.cancel.data:
        return redirect(url_for('staff.applicationtype'))
    return render_template('staff/edit_applicationtype.html', title='Edit Types', form=form)




@staff.route('/applicationtype/<id>/delete', methods=['GET', 'POST'])
@requires_roles('admin')
@login_required
def delete(id):
    app = Application.query.filter_by(applicationtype_id=id).first()
    if app is not None:
        flash("Please withdraw all application with this type then delete ", "danger")
        return redirect(url_for('main.index')) 
    if ApplicationType.query.filter_by(id=id).delete():
        db.session.commit()
        flash ('Type has been deleted', 'success')
        return redirect(url_for('staff.applicationtype'))
    return redirect(url_for('staff.applicationtype'))

@staff.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    applications = None
    target_string = request.form['search']

    applications = Application.query.filter(
        or_(
            Application.tasterday_id.contains(target_string),
            Application.first_name.contains(target_string),
            Application.last_name.contains(target_string)
           
            )
        ).all()

    if target_string == '':
        
        
        search_msg = f'No record(s) found - displaying all {len(applications)} records'
        color = 'danger'
    else:
        search_msg = f'{len(applications)} application(s) found'
        color = 'success'
    return render_template('staff/search.html', 
        title='Search result', applications=applications, 
        search_msg=search_msg, color=color
    )


@staff.route('/staff/<id>/edit_response', methods=['GET', 'POST'])
@requires_roles('admin')
@login_required
def edit_response(id):
    response = Response.query.filter_by(tasterday_id=id, user_id=current_user.get_id())[0]
    form = ResponseForm()
    if request.method == 'GET':
        form.text.data = response.text 
    if form.validate_on_submit() and request.method == 'POST':
        response.text = form.text.data
        db.session.commit()
        return redirect(url_for('staff.get_tasterday', id=id)) 
    return render_template('staff/edit_responce.html', title="Edit response", form=form, id=id)

@staff.route('/staff/<id1>/delete_response/<id2>', methods=['GET', 'POST'])
@requires_roles('admin')
@login_required
def delete_response(id1, id2):
    if Response.query.filter_by(id=id2).delete():
        db.session.commit()
        flash ('Response has been deleted', 'success')
        return redirect(url_for('staff.get_tasterday', id=id1))
    return redirect(url_for('staff.get_tasterday', id=id1))  

