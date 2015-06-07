from flask import Blueprint, render_template, g, request, redirect, url_for, session
from jinja2 import TemplateNotFound

from flask_mail import Message


from flask.ext.security.decorators import login_required
from flask.ext.security import current_user


from tacsite.forms import RegistrationForm, ContactForm, MessageForm
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
    edit_form = RegistrationForm()

    if message_form.validate_on_submit():
        session['scroll_to'] = 'message_success'
        pass

    if edit_form.validate_on_submit():
        session['scroll_to'] = 'edit_success'
        pass

    teams = Team.all()

    free_places = 24 - len(teams)

    try:
        del session['scroll_to']
    except KeyError, e:
        pass

    return render_template('admin.html', teams=teams, free_places=free_places,
                           edit_form=edit_form, message_form=message_form)




@frontend.route("/mail")
def mailsender():
    msg = Message("Hello",
                  recipients=["marcel@quiqua.com"])
    mail.send(msg)
    return 'sent'