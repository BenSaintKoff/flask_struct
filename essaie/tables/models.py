'''
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

Base = declarative_base()
'''

from flask_login import current_user, UserMixin
from .. import db
import datetime


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(20))
    prenom = db.Column(db.String(50))
    mail = db.Column(db.String(100))
    matricule = db.Column(db.String(10))
    mot_de_passe = db.Column(db.String(255))
    #role_id = db.Column(db.Integer(), db.ForeignKey('roles.id', ondelete='CASCADE'))
    role = db.relationship('Role', secondary='user_roles')


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)

    def __repr__(self):
        return "<Role {}>".format(self.name)


class UserRoles(db.Model):
    __tablename__ = 'user_roles'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('roles.id', ondelete='CASCADE'))



