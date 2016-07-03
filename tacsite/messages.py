# -*- coding: utf-8 -*-

from flask_mail import Message

from tacsite.extensions import mail

def send_registration_mail(team):

    p1 = team.persons[0]
    p2 = team.persons[1]
    message_content = u"""\
        Hallo %s und %s,
        schön dass ihr bei unserem Turnier mitmachen wollt.

        Euer Team %s ist registriert.
        Um die Anmeldung abzuschließen, bitten wir euch noch
        die Teilnahmegebühr von 15€ auf folgendes Konto zu überweisen.

        Konto-Inhaber: Alexander Flesch
        IBAN: DE 5612 0965 9700 0124 9282
        BIC: GENODEF1S10

        Gebt als Verwendungszweck bitte "TAC %s" an.


        Falls nach 10 Tagen noch keine Überweisung eingegangen ist,
        verfällt eure Anmeldung.


        Hier nochmal die wichtigsten Informationen zum Turnier:
        - Wann: 17.09.2016, 9 Uhr - Spielbeginn 9:30 Uhr
        - Wo: Modersohnstraße 55, 10245 Berlin
        - Abmeldungen: Bitte bis spätestens 26.08.2015

        Für weitere Fragen stehen wir gern zur Verfügung,
        ihr könnt uns über diese Email-Adresse (tac@quiqua.eu)
        oder die Webseite (tac.quiqua.eu) erreichen.


        Viele Grüße,
        Alex und Marcel
        """ % (p1.first_name, p2.first_name, team.name, team.name)

    recipients = [p1.email_address, p2.email_address]

    msg = Message(body=message_content,
                  subject='Anmeldung TAC Turnier Berlin',
                  recipients=list(set(recipients)),
                  cc=['tac@quiqua.eu'])
    mail.send(msg)


def send_contact_admin_mail(contact_form):
    message_content = 'Absender: ' + contact_form.name.data + '\n'
    message_content += 'Email-Adresse: ' + contact_form.email.data + '\n'
    message_content += 'Telefon: ' + contact_form.phone.data + '\n'
    message_content += '\n' + contact_form.message.data
    msg = Message(body=message_content,
                  subject='Kontakt-Formular',
                  recipients=['tac@quiqua.eu'])

    mail.send(msg)


def send_all_teams_mail(message_form, teams):
    message_content = message_form.message.data

    email_addresses = []

    for team in teams:
        for person in team.persons:
            email_addresses.append(person.email_address)

    msg = Message(body=message_content,
                  subject='Nachricht zum TAC-Turnier Berlin',
                  recipients=list(set(email_addresses)),
                  cc=['tac@quiqua.eu'])

    mail.send(msg)




