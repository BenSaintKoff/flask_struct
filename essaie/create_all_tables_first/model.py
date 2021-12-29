from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine


Base = declarative_base()

from flask_login import current_user, UserMixin
from .. import db
import datetime


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    nom = Column(String(20))
    prenom = Column(String(50))
    mail = Column(String(100))
    matricule = Column(String(10))
    mot_de_passe = Column(String(255))
    # role_id = db.Column(db.Integer(), db.ForeignKey('roles.id', ondelete='CASCADE'))
    role=db.relationship('Role', secondary='user_roles')


class Role(Base):
    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)

    def __repr__(self):
        return "<Role {}>".format(self.name)


class UserRoles(Base):
    __tablename__ = 'user_roles'
    id = Column(Integer, primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('roles.id', ondelete='CASCADE'))



DATABASE_URI = 'postgres+psycopg2://postgres:Mpe.0123456789@localhost:5432/angalia'

engine = create_engine(DATABASE_URI)

# Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)





