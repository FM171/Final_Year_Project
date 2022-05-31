from flask import Blueprint, render_template, redirect, url_for, request
from flask_paginate import Pagination, get_page_args
from app.models import User, TasterDay, Application, ApplicationType, RejectedApplication

main = Blueprint('main', __name__)

@main.route('/')
@main.route('/index', methods=['GET', 'POST'])
@main.route('/index/<cat>', methods=['GET', 'POST'])
def index(cat=None):
    page = int(request.args.get('page', 1))
    per_page = 10
    offset = (page - 1) * per_page

    tasterdays = TasterDay.query.order_by(TasterDay.title.asc())
    applications = Application.query.order_by(Application.last_name.asc())
    types = [cat.name for cat in ApplicationType.query.all()]
    if cat is not None:
        applications = [b.application.order_by(Application.last_name.asc()) for b in ApplicationType.query.filter_by(name=cat)][0]

    applications_for_render = applications.limit(per_page).offset(offset)
    search =False
    q = request.args.get('q')
    if q:
        search=True
    pagination = Pagination(
        page=page, 
        per_page=per_page,
        offset=offset,
        total=applications.count(),
        css_framework='bootstrap3',
        search=search
        )

    return render_template('index.html', applications=applications_for_render,
    pagination=pagination, types=types, tasterdays=tasterdays, title='Home')



