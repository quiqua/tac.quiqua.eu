# -*- coding: utf-8 -*-

from flask.ext.security import SQLAlchemyUserDatastore, UserMixin, RoleMixin
from flask.ext.principal import Permission, Need
from flask.ext.wtf import Form

from sqlalchemy import orm
from wtforms import ValidationError

from sqlalchemy.exc import IntegrityError

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
        try:
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
        except IntegrityError:
            db.session.rollback()
            return {'team': [u'Teamname bereits vergeben.']}


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


roles_users = db.Table('roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
)

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __str__(self):
        return 'Role(%s)' % (self.name,)

    @classmethod
    def by_id(cls, primary_key):
        return Role.query.filter(Role.id == primary_key).first()

    @classmethod
    def by_name(cls, name):
        return Role.query.filter(Role.name == name).first()


class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())

    last_login_at = db.Column(db.DateTime())
    current_login_at = db.Column(db.DateTime())
    current_login_ip = db.Column(db.String(32))
    last_login_ip = db.Column(db.String(32))
    login_count = db.Column(db.Integer())
    timezone = db.Column(db.String(64))

    roles = db.relationship('Role', secondary=roles_users,
                          backref=db.backref('users', lazy='dynamic'))

    # SQLAlchemy wont call __init__ when reconstructing objects from the
    # DB. SQLAlchemy calls this method every time a new object is created
    @orm.reconstructor
    def initialize_on_load(self):
        self._provides_need_set = None

    @property
    def provides_need(self):
        # if permissions for a role are changed during runtime, the user
        # needs to login again
        if self._provides_need_set is None:
            provided_need = set()

            for role in self.roles:
            # add permissions for each role
                role_provides_need = set()
                for perm_need in role.permission_need:
                    role_provides_need.add(Need(perm_need.method, perm_need.value))

                provided_need = provided_need | role_provides_need

            self._provides_need_set = provided_need
        return self._provides_need_set

    def __str__(self):
        return 'User(%s)' % (self.name,)


permissions_roles = db.Table('permission_roles',
    db.Column('permission_need_id', db.Integer(), db.ForeignKey('permission_need.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
)

class PermissionNeed(db.Model):
    """A required need
    This is just a named tuple, and practically any tuple will do.
    The ``method`` attribute can be used to look up element 0, and the ``value``
    attribute can be used to look up element 1.

    The type attribute is used for ItemNeeds, e.g. Need('update', 27, 'post')
    or any other named tuple ('foo', 'bar', 'baz')
    """
    id = db.Column(db.Integer(), primary_key=True)
    method = db.Column(db.String(20), nullable=False)
    value = db.Column(db.String(50), nullable=False)
    type = db.Column(db.String(50))

    roles = db.relationship('Role', secondary=permissions_roles,
                          backref=db.backref('permission_need', lazy='dynamic'))

    def __str__(self):
        return 'Need(%s, %s)' % (self.method, self.value)

user_datastore = SQLAlchemyUserDatastore(db, User, Role)




