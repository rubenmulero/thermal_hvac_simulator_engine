"""
This file contains the models needed to store some basic data using SQLITE database.

The basic idea is to have the user information inside a simple database

"""

from flask_sqlalchemy import SQLAlchemy

class Models():

    def __init__(self, p_app):
        self.db = SQLAlchemy(p_app)

    def get_db_object(self):
        return self.db

    # roles_users = db.Table('roles_users',
    #         db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    #         db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))
    #
    # class Role(db.Model, RoleMixin):
    #     id = db.Column(db.Integer(), primary_key=True)
    #     name = db.Column(db.String(80), unique=True)
    #     description = db.Column(db.String(255))
    #
    # class User(db.Model, UserMixin):
    #     id = db.Column(db.Integer, primary_key=True)
    #     email = db.Column(db.String(255), unique=True)
    #     password = db.Column(db.String(255))
    #     active = db.Column(db.Boolean())
    #     confirmed_at = db.Column(db.DateTime())
    #     roles = db.relationship('Role', secondary=roles_users,
    #                             backref=db.backref('users', lazy='dynamic'))

