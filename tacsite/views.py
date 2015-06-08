from flask import Blueprint, render_template, g, request, redirect, url_for, session, flash
from jinja2 import TemplateNotFound

from flask_mail import Message


from flask.ext.security.decorators import login_required
from flask.ext.security import current_user


from tacsite.forms import RegistrationForm, ContactForm, MessageForm, EditForm
from tacsite.models import Person, Team
from tacsite.extensions import mail

frontend = Blueprint('frontend', __name__, template_folder='templates')

@frontend.route('/', methods=['GET', 'POST'])
def index():
    reg_form = RegistrationForm()
    contact_form = ContactForm()

    teams = Team.all()

    free_places = 24 - len(teams)

    if free_places < 0:
        free_places = 0
    if free_places > 0:
        if reg_form.validate_on_submit():
            team = Team.create_from_registration(reg_form, store=True)
            teams = Team.all()
            free_places = free_places - 1

            session['scroll_to'] = 'reg_success'
            return redirect(url_for('frontend.index'))
        else:
            session['scroll_to'] = 'reg_error'

    if contact_form.validate_on_submit():
        session['scroll_to'] = 'contact_success'
        return redirect(url_for('frontend.index'))


    allow_new = free_places > 0

    scroll_to = session.get('scroll_to')

    try:
        del session['scroll_to']
    except KeyError, e:
        pass


    return render_template('index.html', teams=teams, free_places=free_places,
                           allow_new=allow_new, reg_form=reg_form,
                           contact_form=contact_form, scroll_to=scroll_to)



@frontend.route('/admin', methods=['GET', 'POST'])
def admin():
    message_form = MessageForm()

    if message_form.validate_on_submit():
        session['scroll_to'] = 'message_success'
        pass

    teams = Team.all()

    free_places = 24 - len(teams)

    try:
        del session['scroll_to']
    except KeyError, e:
        pass

    return render_template('admin.html', teams=teams, free_places=free_places,
                           message_form=message_form)


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
        team.update_from_from(form)
        return redirect(url_for('frontend.admin'))

    return render_template('edit_team.html', team=team, edit_form=form)

@frontend.route('/delete/<int:team>')
def delete_team(team):
    return redirect(url_for('frontend.admin'))

@frontend.route('/logout')
def logout():
    return 'bar'

# @frontend.route("/mail")
# def mailsender():
#     msg = Message("Hello",
#                   recipients=["marcel@quiqua.eu"])
#     mail.send(msg)
#     return 'sent'