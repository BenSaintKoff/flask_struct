# -*- coding: utf-8 -*-
"""
Created on Wed Nov  6 14:10:30 2019

@author: 4882
"""
# from flask_ppe import db, create_app
# db.create_all(app=create_app())

# from .tables.models import *

from flask import Flask, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user, AnonymousUserMixin

from flask_jwt_extended import (JWTManager)
from flask_cors import CORS
from flask_admin import Admin
from flask_admin.base import AdminIndexView, expose

from flask_admin.menu import MenuLink
from flask_admin.contrib.sqla import ModelView

# from werkzeug.utils import cached_property

from . import config
from flask_track_usage import TrackUsage

from flask_track_usage.storage.output import OutputWriter

from werkzeug.security import generate_password_hash

AdminIndexView()

import json

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()


class ControlModelView(ModelView):
    can_delete = True
    column_searchable_list = ['id', 'nom', 'prenom', 'matricule']

    def on_model_change(self, form, model, is_created):

        if not model.mot_de_passe.startswith('sha256$'):
            model.mot_de_passe = generate_password_hash(model.mot_de_passe, method='sha256')
        else:
            pass

    def is_accessible(self):
        from .tables.models import Role, UserRoles
        if current_user.is_anonymous == False:
            # if (current_user.is_super_user == True) | (current_user.is_help_desk == True):
            user_role = UserRoles.query.filter_by(user_id=int(current_user.id))
            for ur in user_role:
                r = Role.query.filter_by(id=ur.role_id).first()
                if r.name == 'admin':
                    return current_user.is_authenticated
            return not current_user.is_authenticated


class ControlModelViewRole(ModelView):
    can_delete = True
    column_searchable_list = ['id', 'name']


class ControlModelViewUserRole(ModelView):
    can_delete = True
    column_hide_backrefs = False
    column_searchable_list = ['user_id', 'role_id']


class Anonymous(AnonymousUserMixin):
    def __init__(self):
        self.matricule = 'Guest'


class MyHomeView(AdminIndexView):
    @expose('/')
    def index(self):
        from .tables.models import Role, UserRoles

        if current_user.is_anonymous == False:
            user_role = UserRoles.query.filter_by(user_id=int(current_user.id))
            for ur in user_role:
                r = Role.query.filter_by(id=ur.role_id).first()
                if r.name == 'admin':
                    return self.render('admin/index.html')
            return redirect('/login_admin')

            ''' if (current_user.is_super_user == True) | (current_user.is_help_desk == True):
                            return self.render('admin/index.html')
                            else:
                            return redirect('/login_admin') '''
        else:
            return redirect('/login_admin')


'''logging.basicConfig(level=logging.DEBUG,
                   format='[%(asctime)s]: {} %(levelname)s %(message)s'.format(os.getpid()),
                   datefmt='%Y-%m-%d %H:%M:%S',
                   handlers=[logging.StreamHandler()])

logger = logging.getLogger()'''


def create_app():
    # logger.info(f'Starting app in {config.APP_ENV} environment')
    app = Flask(__name__)
    app.config.from_object('essaie.config')
    '''t = TrackUsage(app, [
        SQLStorage(db=SQLAlchemy(app))
    ])'''
    file_log = open('./essaie/log/usage.log', mode='a+')
    t = TrackUsage(app, [OutputWriter(output=file_log, transform=lambda s: str(s) + '\n')])

    app.config['JWT_TOKEN_LOCATION'] = ['cookies']
    app.config['JWT_COOKIE_CSRF_PROTECT'] = True
    app.config['JWT_SECRET_KEY'] = 'n{yF"M9aK;41$@KeQRA+{[0lDV("51'

    jwt = JWTManager(app)
    CORS(app)

    # db.create_all(app)

    db.init_app(app)

    # db.create_all(app)

    # login = LoginManager(app)

    # login.anonymous_user = Anonymous

    admin = Admin(app, name='Gestion des utilisateurs', template_mode='bootstrap3', index_view=MyHomeView())
    from .tables.models import User, Role, UserRoles
    admin.add_view(ControlModelView(User, db.session))
    admin.add_view(ControlModelViewRole(Role, db.session))
    # admin.add_view(ControlModelViewUserRole(UserRoles, db.session))
    admin.add_link(MenuLink(name='Logout', category='', url="/logout"))

    # blueprint for auth routes in our app
    from .app import main as main_blueprint
    from .auth import auth as auth_blueprint
    from .pilotage import pilotage as pilotage_blueprint

    t.include_blueprint(main_blueprint)
    t.include_blueprint(auth_blueprint)
    t.include_blueprint(pilotage_blueprint)
    app.register_blueprint(main_blueprint)
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(pilotage_blueprint)

    login = LoginManager(app)
    login.anonymous_user = Anonymous
    # login_manager.login_view = 'auth.login'
    # login_manager.init_app(app)

    # blueprint for non-auth parts of app
    '''from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)'''

    from .tables.models import User

    #@jwt.user_claims_loader
    @login.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        u = User.query.filter_by(matricule=user_id).first()
        if u != None:
            return {'matricule': u.matricule}
        else:
            u = User.query.get(user_id)
            return u

    # def shutdown_session(exception=None):

    #     if db.session is not None:
    #         db.session.close()
    #         db.session.remove()

    # app.teardown_appcontext(shutdown_session)

    return app





