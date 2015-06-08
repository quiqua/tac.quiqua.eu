from flask.ext.wtf import Form

from tacsite.extensions import db


team_compositions = db.Table('team_compositions',
    db.Column('team_id', db.Integer, db.ForeignKey('team.id')),
    db.Column('person_id', db.Integer, db.ForeignKey('person.id'))
)


def split_name(name):
    names = name.split(' ')
    name_dict = {}
    if len(names) > 1:
        first_name = names[0]
        last_name = names[-1]
        name_dict['first_name'] = first_name
        name_dict['last_name'] = last_name
    else:
        name_dict['first_name'] = name
        name_dict['last_name'] = None
    return name_dict


class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    payed = db.Column(db.Boolean)
    persons = db.relationship('Person', secondary=team_compositions,
                backref=db.backref('teams', lazy='dynamic'), lazy='dynamic')

    @classmethod
    def by_name(cls, name):
        q = Team.query.filter(Team.name == name)
        return q.first()


    @classmethod
    def by_id(cls, id):
        q = Team.query.filter(Team.id == id)
        return q.first()


    @classmethod
    def all(cls):
        q = Team.query.order_by(Team.name)
        return q.all()

    @classmethod
    def create_from_registration(cls, form, store=True):
        if isinstance(form, Form):
            persons = Person.create_from_registration(form, store=store)

            team = Team(name=form.team.data)
            team.persons = persons

            if store:
                db.session.add(team)
                db.session.commit()

            return team
        return None

    def update_from_from(self, form):
        self.name = form.team.data
        self.payed = form.payed.data
        self.persons[0].raw_name = form.person_one.data
        self.persons[0].email_address = form.email_one.data
        kwargs = split_name(form.person_one.data)
        self.persons[0].first_name = kwargs['first_name']
        self.persons[0].last_name = kwargs['last_name']
        self.persons[1].raw_name = form.person_two.data
        self.persons[1].email_address = form.email_two.data
        kwargs = split_name(form.person_two.data)
        self.persons[1].first_name = kwargs['first_name']
        self.persons[1].last_name = kwargs['last_name']

        db.session.add(self)
        db.session.commit()


class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    raw_name = db.Column(db.String)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    email_address = db.Column(db.String)

    @classmethod
    def create_from_registration(cls, form, store=True):
        if isinstance(form, Form):
            kwargs = split_name(form.person_one.data)
            kwargs['email_address'] = form.email_one.data
            kwargs['raw_name'] = form.person_one.data

            person_one = Person(**kwargs)

            kwargs = split_name(form.person_two.data)
            kwargs['email_address'] = form.email_two.data
            kwargs['raw_name'] = form.person_two.data

            person_two = Person(**kwargs)

            if store:
                db.session.add(person_one)
                db.session.add(person_two)
                db.session.commit()

            return [person_one, person_two]
        return []
