from flask.ext.wtf import Form
from wtforms import TextField, TextAreaField, ValidationError
from wtforms.validators import Required, Email

from tacsite.models import Team, Person


class RegistrationForm(Form):
    team = TextField('Team Name', validators=[Required()])
    person_one = TextField('Spieler 1', validators=[Required()])
    person_two = TextField('Spieler 2', validators=[Required()])
    email_one = TextField('Email Spieler 1', validators=[Required(), Email()])
    email_two = TextField('Email Spieler 2', validators=[Required(), Email()])

    def validate_team(self, field):
        if Team.by_name(field.data):
            raise ValidationError('Teamname bereits vergeben.')


class ContactForm(Form):
    name = TextField('Name', validators=[Required()])
    email = TextField('Email', validators=[Required(), Email()])
    phone = TextField('Telefon')
    message = TextAreaField('Nachricht', validators=[Required()])


class MessageForm(Form):
    message = TextAreaField('Nachricht', validators=[Required()])