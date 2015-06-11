# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, g, jsonify, request, redirect, url_for, session, flash
from jinja2 import TemplateNotFound

from flask_mail import Message


from flask.ext.security.decorators import login_required
from flask.ext.security import current_user
from flask.ext.security.decorators import roles_required, roles_accepted, login_required
from werkzeug.datastructures import MultiDict

from tacsite.forms import RegistrationForm, ContactForm, MessageForm, EditForm
from tacsite.messages import (
        send_contact_admin_mail, send_all_teams_mail, send_registration_mail
)

from tacsite.models import Person, Team

frontend = Blueprint('frontend', __name__, template_folder='templates')


@frontend.route('/', methods=['GET', 'POST'])
def index():
    reg_form = RegistrationForm(prefix='registerteam')
    contact_form = ContactForm(prefix='contactus')

    teams = Team.all()

    free_places = 24 - len(teams)

    if free_places < 0:
        free_places = 0
    if free_places > 0:
        if reg_form.submit.data:
            if reg_form.validate_on_submit():
                team = Team.create_from_registration(reg_form, store=True)
                session['scroll_to'] = 'reg_success'
                send_registration_mail(team)
                return redirect(url_for('frontend.index'))
            else:
                session['scroll_to'] = 'reg_error'

    if contact_form.submit.data:
        if contact_form.validate_on_submit():
            session['scroll_to'] = 'contact_success'
            send_contact_admin_mail(contact_form)
            return redirect(url_for('frontend.index'))
        else:
            session['scroll_to'] = 'contact_error'

    allow_new = free_places > 0
    scroll_to = session.get('scroll_to')
    try:
        del session['scroll_to']
    except KeyError, e:
        pass

    return render_template('index.html', teams=teams, free_places=free_places,
                           allow_new=allow_new, reg_form=reg_form,
                           contact_form=contact_form, scroll_to=scroll_to)


def _render_json(form):
    has_errors = len(form.errors) > 0

    if has_errors:
        code = 422
        response = dict(errors=form.errors)
    else:
        code = 200
        response = dict()

    resp = jsonify(dict(meta=dict(code=code), response=response))
    resp.status_code = code
    return resp


@frontend.route('/admin', methods=['GET', 'POST'])
@login_required
@roles_required('admin')
def admin():
    message_form = MessageForm()
    teams = Team.all()
    free_places = 24 - len(teams)

    if message_form.submit.data:
        if message_form.validate_on_submit():
            send_all_teams_mail(message_form)
            session['scroll_to'] = 'contact_success'
            return redirect(url_for('frontend.admin'))
        else:
            session['scroll_to'] = 'contact_error'
    scroll_to = session.get('scroll_to')
    try:
        del session['scroll_to']
    except KeyError, e:
        pass

    return render_template('admin.html', teams=teams, free_places=free_places,
                           message_form=message_form, scroll_to=scroll_to)

@roles_required('admin')
@frontend.route('/edit/<int:team>', methods=['GET', 'POST'])
def edit_team(team):

    team = Team.by_id(team)

    if team is None:
        flash('Team does not exists')
        return redirect(url_for('frontend.admin'))

    person_one = team.persons[0]
    person_two = team.persons[1]

    team_data = {
        'team': team.name,
        'person_one': person_one.raw_name,
        'person_two': person_two.raw_name,
        'email_one': person_one.email_address,
        'email_two': person_two.email_address,
        'payed': team.payed
    }
    form = EditForm(request.form, data=team_data)

    if form.validate_on_submit():
        err = team.update_from_from(form)
        if err:
            form._errors = err
            form.team.errors = err['team']
            return render_template('edit_team.html', team=team, edit_form=form)

        return redirect(url_for('frontend.admin'))

    return render_template('edit_team.html', team=team, edit_form=form)

@roles_required('admin')
@frontend.route('/delete/<int:team_id>')
def delete_team(team_id):
    team = Team.by_id(team_id)
    if team:
        db.session.delete(team)
        db.session.commit()
    return redirect(url_for('frontend.admin'))

@frontend.route('/impressum')
def impressum():
    return render_template('impressum.html')

